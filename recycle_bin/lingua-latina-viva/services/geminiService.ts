import { GoogleGenAI, Type, Schema } from "@google/genai";
import { MorphAnalysis, QuizQuestion, ExerciseDifficulty, Flashcard } from "../types";
import { VOCABULARY } from "./learningEngine";

// --- Configuration ---

const getClient = () => {
  const apiKey = process.env.API_KEY;
  // If no key is present, return null to trigger offline mode immediately
  if (!apiKey || apiKey.includes("INSERT_API_KEY")) {
    return null;
  }
  return new GoogleGenAI({ apiKey });
};

// --- OFFLINE LOGIC HELPERS ---

const getRandomElement = <T>(arr: T[]): T => arr[Math.floor(Math.random() * arr.length)];

const shuffleArray = <T>(array: T[]): T[] => {
    return array.map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);
};

// 1. Offline Quiz Generator
const generateOfflineQuiz = (difficulty: ExerciseDifficulty): QuizQuestion[] => {
    // Generate 3 questions based on local VOCABULARY
    const questions: QuizQuestion[] = [];
    
    for (let i = 0; i < 3; i++) {
        const targetWord = getRandomElement(VOCABULARY);
        const type = Math.random() > 0.5 ? 'translate_to_es' : 'identify_pos';
        
        if (type === 'translate_to_es') {
            const correct = targetWord.spanish;
            // Get 3 random distractors
            const distractors = shuffleArray(VOCABULARY.filter(w => w.id !== targetWord.id))
                .slice(0, 3)
                .map(w => w.spanish);
            
            questions.push({
                question: `¿Qué significa "${targetWord.latin}"?`,
                options: shuffleArray([correct, ...distractors]),
                correctAnswer: correct,
                explanation: `"${targetWord.latin}" es un ${targetWord.partOfSpeech} que significa "${correct}".`
            });
        } else {
            const correct = targetWord.partOfSpeech;
            const distractors = ["Verbo", "Sustantivo", "Adjetivo", "Adverbio"].filter(d => !correct.includes(d)).slice(0, 3);
            
            questions.push({
                question: `¿Cuál es la categoría gramatical de "${targetWord.latin}"?`,
                options: shuffleArray([correct, ...distractors]),
                correctAnswer: correct,
                explanation: `Se clasifica como ${correct}.`
            });
        }
    }
    return questions;
};

// 2. Offline Analyzer Heuristics
const analyzeOffline = (text: string): MorphAnalysis[] => {
    const words = text.replace(/[.,;?!]/g, '').split(/\s+/);
    
    return words.map((word, index) => {
        const lower = word.toLowerCase();
        // Simple heuristic lookup
        const vocabMatch = VOCABULARY.find(v => lower.startsWith(v.latin.slice(0, -1))); // Basic stem match
        
        let pos = "Desconocido";
        let morph = "N/A";
        let dep = "N/A";
        let expl = "Modo offline: Análisis basado en terminaciones.";
        let trans = vocabMatch ? vocabMatch.spanish : "Traducción no disponible";

        // Heuristics for beginners
        if (lower.endsWith('a')) {
            morph = "Nom Sg Fem / Abl Sg Fem";
            dep = "Sujeto / Circunstancial";
            pos = "Sustantivo";
        } else if (lower.endsWith('am') || lower.endsWith('um') || lower.endsWith('em')) {
            morph = "Acusativo Sg";
            dep = "Objeto Directo";
            pos = "Sustantivo";
        } else if (lower.endsWith('ae') || lower.endsWith('i')) {
            morph = "Genitivo Sg / Nom Pl";
            dep = "Posesión / Sujeto Pl";
            pos = "Sustantivo";
        } else if (lower.endsWith('o') || lower.endsWith('is')) {
            morph = "Dat/Abl";
            dep = "Objeto Indirecto";
        } else if (lower.endsWith('t') || lower.endsWith('nt') || lower.endsWith('mus')) {
            pos = "Verbo";
            dep = "Núcleo del Predicado";
            morph = "Presente Indicativo";
        }

        if (vocabMatch) {
            pos = vocabMatch.partOfSpeech;
        }

        return {
            id: index + 1,
            word: word,
            lemma: vocabMatch ? vocabMatch.latin : word,
            pos: pos,
            morphology: morph,
            dependency: dep,
            headId: 0, // Hard to calc dependency tree offline without heavy logic
            explanation: expl,
            translation: trans
        };
    });
};

// 3. Offline Tutor
const tutorOffline = (history: any[], message: string): string => {
    const msg = message.toLowerCase();
    
    // Check vocab
    const vocabMatch = VOCABULARY.find(v => msg.includes(v.latin) || msg.includes(v.spanish));
    if (vocabMatch) {
        return `He encontrado esto en tu libro: "${vocabMatch.latin}" significa "${vocabMatch.spanish}" (${vocabMatch.partOfSpeech}).`;
    }

    if (msg.includes('hola') || msg.includes('salve')) return "Salve, discipule. (Modo Offline activo)";
    if (msg.includes('gracias')) return "De nada. ¡Sigue estudiando!";
    
    return "Estoy en Modo Offline. Solo puedo ayudarte traduciendo palabras que ya existen en tu vocabulario. Intenta escribir una palabra en latín.";
};

// --- PUBLIC API WRAPPERS ---

export const analyzeLatinText = async (text: string): Promise<MorphAnalysis[]> => {
  if (!text.trim()) return [];

  const ai = getClient();
  if (!ai) return analyzeOffline(text);

  try {
    const analysisSchema: Schema = {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            id: { type: Type.INTEGER, description: "Índice secuencial" },
            word: { type: Type.STRING },
            lemma: { type: Type.STRING },
            pos: { type: Type.STRING },
            morphology: { type: Type.STRING },
            dependency: { type: Type.STRING },
            headId: { type: Type.INTEGER },
            explanation: { type: Type.STRING },
            translation: { type: Type.STRING },
          },
          required: ["id", "word", "lemma", "pos", "morphology", "dependency", "headId", "explanation", "translation"],
        }
    };

    const prompt = `Analiza morfológica y sintácticamente (pedagógico): "${text}"`;
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: analysisSchema,
      }
    });

    const jsonText = response.text;
    if (!jsonText) return analyzeOffline(text);
    return JSON.parse(jsonText) as MorphAnalysis[];
  } catch (error) {
    console.warn("API Error, falling back to offline analysis", error);
    return analyzeOffline(text);
  }
};

export const generateLatinQuiz = async (difficulty: ExerciseDifficulty, topic: string): Promise<QuizQuestion[]> => {
  const ai = getClient();
  if (!ai) return generateOfflineQuiz(difficulty);

  try {
    const quizSchema: Schema = {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            question: { type: Type.STRING },
            options: { type: Type.ARRAY, items: { type: Type.STRING } },
            correctAnswer: { type: Type.STRING },
            explanation: { type: Type.STRING }
          },
          required: ["question", "options", "correctAnswer", "explanation"]
        }
    };

    const prompt = `Generate 3 Latin questions about ${topic} (${difficulty}). Language: Spanish.`;
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: quizSchema,
      }
    });

    const jsonText = response.text;
    if (!jsonText) return generateOfflineQuiz(difficulty);
    return JSON.parse(jsonText) as QuizQuestion[];
  } catch (error) {
    console.warn("API Error, falling back to offline quiz", error);
    return generateOfflineQuiz(difficulty);
  }
};

export const getTutorResponse = async (history: {role: 'user'|'model', text: string}[], message: string) => {
  const ai = getClient();
  if (!ai) return tutorOffline(history, message);

  try {
    const chat = ai.chats.create({
        model: 'gemini-2.5-flash',
        history: history.map(h => ({ role: h.role, parts: [{ text: h.text }] })),
        config: { systemInstruction: "Eres Marcus, profesor de latín." }
    });
    const result = await chat.sendMessage({ message });
    return result.text;
  } catch (error) {
    console.warn("API Error, falling back to offline tutor", error);
    return tutorOffline(history, message);
  }
};