export enum AppView {
  DASHBOARD = 'dashboard',
  LESSON = 'lesson',
  ANALYZER = 'analyzer',
  SRS = 'srs',
  TUTOR = 'tutor',
  EXERCISES = 'exercises',
  READING = 'reading',
  CHALLENGE = 'challenge'
}

export interface MorphAnalysis {
  id: number; // 1-based index based on word order
  word: string;
  lemma: string;
  pos: string; 
  morphology: string;
  dependency: string; // e.g., "Sujeto", "Objeto Directo", "Ablativo Instrumental"
  headId: number; // The 'id' of the word that governs this one (0 for Root)
  explanation: string; // Pedagogical explanation of WHY it has this case/function
  translation: string;
}

export interface Flashcard {
  id: string;
  latin: string;
  spanish: string;
  partOfSpeech: string;
  difficulty: number;
  nextReview: number;
  lessonId: number;
}

export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
  timestamp: number;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: string;
  explanation: string;
}

export enum ExerciseDifficulty {
  BEGINNER = 'Principiante',
  INTERMEDIATE = 'Intermedio',
  ADVANCED = 'Avanzado'
}

// --- New Core Types for the Organic Plan ---

export interface UserProgress {
  currentLesson: number;
  xp: number;
  lessonsCompleted: number[];
  vocabMastery: Record<string, number>; // wordId -> mastery level (0.0 - 1.0)
  exercisesCompleted: Record<number, number>; // lessonId -> count
  readingsCompleted: string[]; // textId[]
  challengesPassed: number[]; // lessonId[]
}

export interface Lesson {
  id: number;
  title: string;
  topic: string;
  description: string;
  content: string; // Markdown/HTML content for grammar theory
  unlockRequirements?: {
    prevLesson?: number;
  };
}

export interface Reading {
  id: string;
  lessonId: number;
  title: string;
  content: string; // The Latin text
  translation: string;
  questions: {
    question: string;
    answer: string;
  }[];
}

export interface Challenge {
  lessonId: number;
  title: string;
  description: string;
  questions: QuizQuestion[];
}

export interface Recommendation {
  id: string;
  type: 'lesson' | 'vocab' | 'exercise' | 'reading' | 'challenge';
  message: string;
  priority: 'high' | 'medium' | 'low';
  actionView: AppView;
  actionPayload?: any; // e.g., specific lesson ID
}