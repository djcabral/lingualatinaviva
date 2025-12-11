import { Lesson, Flashcard, Reading, UserProgress, Recommendation, AppView, Challenge } from '../types';

// --- Static Content (The Curriculum) ---

export const LESSONS: Lesson[] = [
  {
    id: 1,
    title: "Primera Declinación",
    topic: "Sustantivos Femeninos (-a)",
    description: "Aprende los fundamentos de los casos y la primera declinación.",
    content: `
      # La Primera Declinación
      
      El latín utiliza **casos** para indicar la función de una palabra en la oración.
      La primera declinación se caracteriza por la terminación **-a** en el nominativo singular y **-ae** en el genitivo singular.
      
      ## Paradigma: Puella (Niña)
      
      | Caso | Singular | Plural | Función |
      |------|----------|--------|---------|
      | **Nominativo** | puell-a | puell-ae | Sujeto |
      | **Genitivo** | puell-ae | puell-arum | Posesión (de) |
      | **Dativo** | puell-ae | puell-is | Objeto Indirecto (a/para) |
      | **Acusativo** | puell-am | puell-as | Objeto Directo |
      | **Ablativo** | puell-a | puell-is | Circunstancial (con/por) |
    `
  },
  {
    id: 2,
    title: "El Verbo 'Esse' y 1ª Conjugación",
    topic: "Verbos (-are)",
    description: "Acciones básicas y el verbo ser/estar.",
    content: `
      # Verbos de 1ª Conjugación
      
      Terminan en **-are** en infinitivo (ej: *amare*).
      
      ## Presente Indicativo
      | Persona | Latín | Español |
      |---|---|---|
      | 1ª Sg | am-o | Yo amo |
      | 2ª Sg | am-as | Tú amas |
      | 3ª Sg | am-at | Él ama |
      | 1ª Pl | am-amus | Nosotros amamos |
      | 2ª Pl | am-atis | Vosotros amáis |
      | 3ª Pl | am-ant | Ellos aman |
      
      ## Verbo Sum (Ser/Estar)
      Irregular pero esencial: *sum, es, est, sumus, estis, sunt*.
    `,
    unlockRequirements: { prevLesson: 1 }
  },
  {
    id: 3,
    title: "Segunda Declinación (M)",
    topic: "Sustantivos Masculinos (-us/er)",
    description: "El mundo masculino: señores, esclavos y campos.",
    content: `
      # La Segunda Declinación
      
      Principalmente masculina. Termina en **-us** o **-er**.
      
      ## Paradigma: Dominus (Señor)
      
      | Caso | Singular | Plural |
      |------|----------|--------|
      | Nom | domin-us | domin-i |
      | Gen | domin-i | domin-orum |
      | Dat | domin-o | domin-is |
      | Acc | domin-um | domin-os |
      | Abl | domin-o | domin-is |
    `,
    unlockRequirements: { prevLesson: 2 }
  },
  {
    id: 4,
    title: "Segunda Declinación (N)",
    topic: "Sustantivos Neutros (-um)",
    description: "Objetos inanimados, guerras y regalos.",
    content: `
      # El Género Neutro
      
      En latín, además de masculino y femenino, existe el neutro.
      La regla de oro del neutro: **El Nominativo y el Acusativo son siempre iguales**. En plural, terminan en **-a**.
      
      ## Paradigma: Bellum (Guerra)
      
      | Caso | Singular | Plural |
      |------|----------|--------|
      | Nom | bell-um | bell-a |
      | Acc | bell-um | bell-a |
      | Gen | bell-i | bell-orum |
    `,
    unlockRequirements: { prevLesson: 3 }
  },
  {
    id: 5,
    title: "Adjetivos de 1ª y 2ª Clase",
    topic: "Concordancia (-us, -a, -um)",
    description: "Describiendo el mundo: bueno, malo, grande, pequeño.",
    content: `
      # Adjetivos 2-1-2
      
      Los adjetivos deben concordar en **Género, Número y Caso** con el sustantivo que modifican.
      
      * *Puer bonus* (Niño bueno - Masc)
      * *Puella bona* (Niña buena - Fem)
      * *Donum bonum* (Regalo bueno - Neutro)
    `,
    unlockRequirements: { prevLesson: 4 }
  },
  // --- Bloque 2: Expansión Gramatical (Lecciones 6-10) ---
  { id: 6, title: "Segunda Conjugación", topic: "Verbos en -ēre (Moneo)", description: "Verbos con vocal temática E larga.", content: "# Segunda Conjugación\n\nInfinitivo en **-ēre**. \n\nEjemplo: *Monere* (Advertir).\n* Moneo, Mones, Monet..." },
  { id: 7, title: "Tercera Declinación (Consonate)", topic: "Rex, Miles, Corpus", description: "La declinación más grande y diversa.", content: "# Tercera Declinación\n\nGenitivo termina en **-is**. \n\nEjemplo: *Rex, Regis* (Rey)." },
  { id: 8, title: "Tercera Conjugación", topic: "Verbos en -ere (Rego)", description: "La conjugación breve.", content: "# Tercera Conjugación\n\nInfinitivo en **-ĕre** (e breve).\n* Rego, Regis, Regit..." },
  { id: 9, title: "Tercera Declinación (Temas en -i)", topic: "Civis, Mare, Urbs", description: "Reglas especiales para ciertos sustantivos.", content: "# Temas en -i\n\nGenitivo plural en **-ium**.\nNeutros nominativo en **-ia**." },
  { id: 10, title: "Cuarta Conjugación", topic: "Verbos en -ire (Audio)", description: "Verbos con vocal temática I.", content: "# Cuarta Conjugación\n\nInfinitivo en **-ire**.\n* Audio, Audis, Audit..." },

  // --- Bloque 3: Tiempos del Pasado y Futuro (Lecciones 11-15) ---
  { id: 11, title: "El Imperfecto", topic: "Ba-bam-bas-bat", description: "Acciones continuas en el pasado.", content: "# Imperfecto Indicativo\n\nSe forma con el infijo **-ba-**.\n* Amabam (Yo amaba)\n* Videbam (Yo veía)" },
  { id: 12, title: "El Futuro Imperfecto (1ª/2ª)", topic: "Bo-bis-bit", description: "Futuro para conjugaciones 1 y 2.", content: "# Futuro (Tipo 1)\n\nUtiliza **-bo, -bis, -bit**.\n* Amabo (Amaré)" },
  { id: 13, title: "El Futuro Imperfecto (3ª/4ª)", topic: "Am-es-et", description: "Futuro para conjugaciones 3 y 4.", content: "# Futuro (Tipo 2)\n\nUtiliza **-am, -es, -et**.\n* Regam (Gobernaré), Reges (Gobernarás)." },
  { id: 14, title: "El Perfecto Activo", topic: "Acción Puntual (-i, -isti, -it)", description: "El pasado simple o perfecto.", content: "# Perfecto\n\nIndica acción terminada.\nTerminaciones: **-i, -isti, -it, -imus, -istis, -erunt**." },
  { id: 15, title: "Pronombres Personales", topic: "Ego, Tu, Nos, Vos", description: "Yo, tú, nosotros, vosotros y sus casos.", content: "# Pronombres\n\n* Ego (Yo), Mei (De mí), Mihi (A mí), Me (Me), Me (Por mí)." },

  // --- Bloque 4: Complejidad Sintáctica (Lecciones 16-20) ---
  { id: 16, title: "Adjetivos de 3ª Declinación", topic: "Omnis, Ingens, Felix", description: "Adjetivos que siguen la tercera declinación.", content: "# Adjetivos de 3ª\n\nSiguen patrones de temas en -i." },
  { id: 17, title: "Demostrativos I", topic: "Hic, Haec, Hoc", description: "Este, esta, esto.", content: "# Hic, Haec, Hoc\n\nSeñalan cercanía al hablante." },
  { id: 18, title: "Demostrativos II", topic: "Ille, Illa, Illud", description: "Aquel, aquella, aquello.", content: "# Ille, Illa, Illud\n\nSeñalan lejanía." },
  { id: 19, title: "Cuarta Declinación", topic: "Sustantivos en -us (Manus)", description: "La declinación de la 'u'.", content: "# Cuarta Declinación\n\nGenitivo en **-us**.\nEj: Manus, Exercitus." },
  { id: 20, title: "Quinta Declinación", topic: "Sustantivos en -es (Res)", description: "La declinación de la 'e'.", content: "# Quinta Declinación\n\nGenitivo en **-ei**.\nEj: Res, Dies." },

  // --- Bloque 5: Voz Pasiva (Lecciones 21-25) ---
  { id: 21, title: "Voz Pasiva (Presente)", topic: "R-ris-tur", description: "Ser amado, ser visto.", content: "# Voz Pasiva\n\nSujeto recibe la acción.\n* Amor (Soy amado)\n* Amaris (Eres amado)" },
  { id: 22, title: "Voz Pasiva (Perfecto)", topic: "Participio + Sum", description: "Fui amado, he sido visto.", content: "# Pasiva Perfecta\n\nUsa participio perfecto + verbo sum.\n* Amatus sum (Fui amado)." },
  { id: 23, title: "Ablativo Absoluto", topic: "Construcción Gramatical", description: "La estructura más famosa del latín.", content: "# Ablativo Absoluto\n\nSustantivo + Participio en ablativo, independientes de la oración principal.\n* *Urbe capta*, hostes fugerunt (Capturada la ciudad, los enemigos huyeron)." },
  { id: 24, title: "Participios", topic: "Presente, Perfecto, Futuro", description: "Verbos que actúan como adjetivos.", content: "# Participios\n\n* Presente: Amans (Amante)\n* Perfecto: Amatus (Amado)\n* Futuro: Amaturus (El que amará)" },
  { id: 25, title: "Infinitivos", topic: "Formas y Usos", description: "Amar, haber amado, haber de amar.", content: "# Infinitivos\n\nExisten formas activas y pasivas para Presente, Perfecto y Futuro." },

  // --- Bloque 6: Subordinación (Lecciones 26-30) ---
  { id: 26, title: "Oración de Infinitivo", topic: "Acusativo + Infinitivo", description: "Estilo indirecto: 'Dice que él viene'.", content: "# Estilo Indirecto\n\nSujeto en Acusativo, Verbo en Infinitivo.\n* Dicit se venire (Dice que él viene)." },
  { id: 27, title: "Comparativos y Superlativos", topic: "Altior, Altissimus", description: "Más alto, el más alto.", content: "# Grados del Adjetivo\n\n* Comparativo: -ior\n* Superlativo: -issimus" },
  { id: 28, title: "Subjuntivo Presente", topic: "We beat a giant liar", description: "Cambio de vocal para el modo de la irrealidad.", content: "# Subjuntivo Presente\n\nCambio de vocal:\n* 1ª: a -> e (Amem)\n* 2ª: e -> ea (Moneam)" },
  { id: 29, title: "Subjuntivo Imperfecto", topic: "Infinitivo + terminación", description: "Formación sencilla del pasado subjuntivo.", content: "# Subjuntivo Imperfecto\n\nInfinitivo completo + m, s, t...\n* Amarem, Amares, Amaret." },
  { id: 30, title: "Cláusulas Finales (Ut/Ne)", topic: "Propósito", description: "Para que...", content: "# Ut Final\n\n* Venit ut videat (Viene para ver)." },

  // --- Bloque 7: Estructuras Avanzadas (Lecciones 31-35) ---
  { id: 31, title: "Cláusulas Consecutivas", topic: "Ut + Subjuntivo", description: "Tan... que...", content: "# Consecutivas\n\nTam, Ita, Sic + Ut.\n* Tam fessus est ut dormiat (Está tan cansado que duerme)." },
  { id: 32, title: "Cum Histórico", topic: "Cum + Subjuntivo", description: "Cuando/Como...", content: "# Cum Histórico\n\nNarra circunstancias en el pasado." },
  { id: 33, title: "Preguntas Indirectas", topic: "Quis, Quid + Subjuntivo", description: "Me pregunto quién es.", content: "# Interrogativa Indirecta\n\nSiempre lleva verbo en subjuntivo." },
  { id: 34, title: "Gerundio y Gerundivo", topic: "Sustantivo y Adjetivo Verbal", description: "-ndum", content: "# Gerundio\n\nSustantivo verbal.\n* Ars amandi (El arte de amar)." },
  { id: 35, title: "Verbos Deponentes", topic: "Forma pasiva, significado activo", description: "Sequor, Loquor", content: "# Deponentes\n\nParecen pasivos pero se traducen activos.\n* Loquor (Hablo)." },

  // --- Bloque 8: Maestría (Lecciones 36-40) ---
  { id: 36, title: "Perifrástica Pasiva", topic: "Gerundivo + Sum", description: "Obligación: 'Delenda est Carthago'.", content: "# Perifrástica Pasiva\n\nIndica obligación.\n* Hoc faciendum est (Esto debe hacerse)." },
  { id: 37, title: "Oraciones Condicionales", topic: "Si...", description: "Reales, Posibles e Irreales.", content: "# Condicionales\n\n* Si hoc facit, errat (Si hace esto, se equivoca)." },
  { id: 38, title: "Verbos Irregulares Avanzados", topic: "Fero, Volo, Nolo, Malo", description: "Verbos comunes con formas extrañas.", content: "# Irregulares\n\n* Fero (Llevar)\n* Volo (Querer)" },
  { id: 39, title: "Supino", topic: "-um, -u", description: "Propósito y especificación.", content: "# Supino\n\n* Mirabile dictu (Admirable de decir)." },
  { id: 40, title: "Lectura Avanzada", topic: "Literatura Real", description: "Introducción a César y Cicerón.", content: "# Literatura\n\nAnálisis de textos originales sin simplificar." }
];

// --- Vocabulary Generator for Scalability ---

// Manual vocab for first few lessons to ensure quality start
const BASE_VOCABULARY: Flashcard[] = [
  // L1
  { id: 'l1-1', latin: 'puella', spanish: 'niña', partOfSpeech: 'Sustantivo 1ª', difficulty: 1, nextReview: 0, lessonId: 1 },
  { id: 'l1-2', latin: 'roma', spanish: 'roma', partOfSpeech: 'Sustantivo 1ª', difficulty: 1, nextReview: 0, lessonId: 1 },
  { id: 'l1-3', latin: 'via', spanish: 'camino', partOfSpeech: 'Sustantivo 1ª', difficulty: 1, nextReview: 0, lessonId: 1 },
  // L2
  { id: 'l2-1', latin: 'amare', spanish: 'amar', partOfSpeech: 'Verbo 1ª', difficulty: 1, nextReview: 0, lessonId: 2 },
  { id: 'l2-2', latin: 'video', spanish: 'ver', partOfSpeech: 'Verbo 2ª', difficulty: 1, nextReview: 0, lessonId: 2 }, // Actually L6 but useful preview
  { id: 'l2-3', latin: 'est', spanish: 'es', partOfSpeech: 'Verbo Sum', difficulty: 1, nextReview: 0, lessonId: 2 },
  // L3
  { id: 'l3-1', latin: 'dominus', spanish: 'señor', partOfSpeech: 'Sustantivo 2ª', difficulty: 1, nextReview: 0, lessonId: 3 },
  { id: 'l3-2', latin: 'servus', spanish: 'esclavo', partOfSpeech: 'Sustantivo 2ª', difficulty: 1, nextReview: 0, lessonId: 3 },
  // L4
  { id: 'l4-1', latin: 'bellum', spanish: 'guerra', partOfSpeech: 'Sustantivo N', difficulty: 1, nextReview: 0, lessonId: 4 },
  { id: 'l4-2', latin: 'donum', spanish: 'regalo', partOfSpeech: 'Sustantivo N', difficulty: 1, nextReview: 0, lessonId: 4 },
  { id: 'l4-3', latin: 'templum', spanish: 'templo', partOfSpeech: 'Sustantivo N', difficulty: 1, nextReview: 0, lessonId: 4 },
  // L5
  { id: 'l5-1', latin: 'bonus', spanish: 'bueno', partOfSpeech: 'Adjetivo', difficulty: 1, nextReview: 0, lessonId: 5 },
  { id: 'l5-2', latin: 'magnus', spanish: 'grande', partOfSpeech: 'Adjetivo', difficulty: 1, nextReview: 0, lessonId: 5 },
  { id: 'l5-3', latin: 'parvus', spanish: 'pequeño', partOfSpeech: 'Adjetivo', difficulty: 1, nextReview: 0, lessonId: 5 },
];

// Procedural generation for remaining lessons (6-40) to ensure app functionality
const GENERATED_VOCAB: Flashcard[] = [];
for (let i = 6; i <= 40; i++) {
  GENERATED_VOCAB.push(
    { id: `l${i}-1`, latin: `exemplum ${i}a`, spanish: `ejemplo ${i}a`, partOfSpeech: 'General', difficulty: 1, nextReview: 0, lessonId: i },
    { id: `l${i}-2`, latin: `exemplum ${i}b`, spanish: `ejemplo ${i}b`, partOfSpeech: 'General', difficulty: 2, nextReview: 0, lessonId: i },
    { id: `l${i}-3`, latin: `exemplum ${i}c`, spanish: `ejemplo ${i}c`, partOfSpeech: 'General', difficulty: 1, nextReview: 0, lessonId: i }
  );
}

export const VOCABULARY: Flashcard[] = [...BASE_VOCABULARY, ...GENERATED_VOCAB];

// --- Readings & Challenges ---

const BASE_READINGS: Reading[] = [
  {
    id: 'r1',
    lessonId: 1,
    title: 'Roma et Italia',
    content: "Roma in Italia est. Italia terra est. Via est longa. Puella in via est.",
    translation: "Roma está en Italia. Italia es una tierra. El camino es largo. La niña está en el camino.",
    questions: [
      { question: "¿Dónde está Roma?", answer: "En Italia" },
      { question: "¿Cómo es el camino?", answer: "Largo" }
    ]
  },
  {
    id: 'r2',
    lessonId: 2,
    title: 'Iulia et Aemilia',
    content: "Iulia puella est. Aemilia femina est. Iulia Aemiliam amat. Aemilia laborat.",
    translation: "Julia es una niña. Aemilia es una mujer. Julia ama a Aemilia. Aemilia trabaja.",
    questions: [
      { question: "¿Quién trabaja?", answer: "Aemilia" },
      { question: "¿A quién ama Julia?", answer: "A Aemilia" }
    ]
  },
  {
    id: 'r3',
    lessonId: 3,
    title: 'Dominus et Servi',
    content: "Dominus in horto est. Servi laborant. Dominus servos monet.",
    translation: "El señor está en el jardín. Los esclavos trabajan. El señor advierte a los esclavos.",
    questions: [
      { question: "¿Dónde está el señor?", answer: "En el jardín" },
      { question: "¿Qué hacen los esclavos?", answer: "Trabajan" }
    ]
  },
  {
    id: 'r4',
    lessonId: 4,
    title: 'Bellum Romanum',
    content: "Bellum est malum. Romani oppida oppugnant. Templa sunt sacra.",
    translation: "La guerra es mala. Los romanos atacan las ciudades. Los templos son sagrados.",
    questions: [
      { question: "¿Cómo es la guerra?", answer: "Mala" },
      { question: "¿Qué son sagrados?", answer: "Los templos" }
    ]
  },
  {
    id: 'r5',
    lessonId: 5,
    title: 'Villa Magna',
    content: "Villa est magna et pulchra. Hortus est parvus sed bonus.",
    translation: "La villa es grande y hermosa. El jardín es pequeño pero bueno.",
    questions: [
      { question: "¿Cómo es la villa?", answer: "Grande y hermosa" },
      { question: "¿Cómo es el jardín?", answer: "Pequeño" }
    ]
  }
];

const GENERATED_READINGS: Reading[] = [];
for (let i = 6; i <= 40; i++) {
  GENERATED_READINGS.push({
    id: `r${i}`,
    lessonId: i,
    title: `Lectura Lección ${i}`,
    content: `Hoc est exemplum lectionis ${i}. Latine legere bonum est. Discipuli student.`,
    translation: `Este es un ejemplo de la lección ${i}. Leer latín es bueno. Los estudiantes estudian.`,
    questions: [
      { question: "¿Qué es bueno?", answer: "Leer latín" },
      { question: "¿Qué hacen los estudiantes?", answer: "Estudian" }
    ]
  });
}

export const READINGS: Reading[] = [...BASE_READINGS, ...GENERATED_READINGS];

const BASE_CHALLENGES: Challenge[] = [
  {
    lessonId: 1,
    title: "Maestro de la 1ª Declinación",
    description: "Demuestra que dominas los casos y el vocabulario básico.",
    questions: [
      { question: "¿Cuál es el caso del Sujeto?", options: ["Nominativo", "Acusativo", "Dativo", "Ablativo"], correctAnswer: "Nominativo", explanation: "Sujeto = Nominativo." },
      { question: "Traduce: 'Puella rosam amat'", options: ["La niña ama la rosa", "La rosa ama a la niña", "Las niñas aman las rosas"], correctAnswer: "La niña ama la rosa", explanation: "Puella (Nom) hace la acción." },
      { question: "Genitivo singular de 'Puella'", options: ["Puellae", "Puella", "Puellam"], correctAnswer: "Puellae", explanation: "1ª declinación Gen Sg es -ae." }
    ]
  },
  {
    lessonId: 2,
    title: "Maestro de Verbos I",
    description: "Domina el presente y 'Sum'.",
    questions: [
        { question: "'Laboramus' significa...", options: ["Trabajamos", "Trabajo", "Trabajan"], correctAnswer: "Trabajamos", explanation: "-mus es nosotros." },
        { question: "3ª Plural de Sum", options: ["Sunt", "Est", "Sumus"], correctAnswer: "Sunt", explanation: "Ellos son." },
        { question: "Infinitivo de 1ª conjugación", options: ["-are", "-ere", "-ire"], correctAnswer: "-are", explanation: "Ej: Amare." }
    ]
  }
];

const GENERATED_CHALLENGES: Challenge[] = [];
for (let i = 3; i <= 40; i++) {
   GENERATED_CHALLENGES.push({
     lessonId: i,
     title: `Desafío Lección ${i}`,
     description: "Prueba tus conocimientos de esta lección.",
     questions: [
       { question: "¿Pregunta de prueba 1?", options: ["Correcta", "Incorrecta", "Falsa"], correctAnswer: "Correcta", explanation: "Explicación genérica." },
       { question: "¿Pregunta de prueba 2?", options: ["Correcta", "Incorrecta", "Falsa"], correctAnswer: "Correcta", explanation: "Explicación genérica." },
       { question: "¿Pregunta de prueba 3?", options: ["Correcta", "Incorrecta", "Falsa"], correctAnswer: "Correcta", explanation: "Explicación genérica." }
     ]
   });
}

export const CHALLENGES: Challenge[] = [...BASE_CHALLENGES, ...GENERATED_CHALLENGES];

// --- Engine Logic ---

const INITIAL_PROGRESS: UserProgress = {
  currentLesson: 1,
  xp: 0,
  lessonsCompleted: [],
  vocabMastery: {},
  exercisesCompleted: {},
  readingsCompleted: [],
  challengesPassed: []
};

const STORAGE_KEY = 'lingua_latina_progress_v3_full'; // Changed key to force reset with new structure if needed

export const getProgress = (): UserProgress => {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : INITIAL_PROGRESS;
};

export const saveProgress = (progress: UserProgress) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
};

export const completeLesson = (lessonId: number) => {
  const p = getProgress();
  if (!p.lessonsCompleted.includes(lessonId)) {
    p.lessonsCompleted.push(lessonId);
    p.xp += 100;
    saveProgress(p);
  }
};

export const updateVocabMastery = (wordId: string, success: boolean) => {
  const p = getProgress();
  const current = p.vocabMastery[wordId] || 0;
  const newValue = success ? Math.min(1, current + 0.25) : Math.max(0, current - 0.1);
  p.vocabMastery[wordId] = newValue;
  saveProgress(p);
};

export const incrementExerciseCount = (lessonId: number, score: number) => {
  const p = getProgress();
  const current = p.exercisesCompleted[lessonId] || 0;
  p.exercisesCompleted[lessonId] = current + 1;
  p.xp += score * 10;
  saveProgress(p);
};

export const completeReading = (readingId: string) => {
  const p = getProgress();
  if (!p.readingsCompleted.includes(readingId)) {
    p.readingsCompleted.push(readingId);
    p.xp += 50;
    saveProgress(p);
  }
};

export const passChallenge = (lessonId: number) => {
    const p = getProgress();
    if (!p.challengesPassed.includes(lessonId)) {
        p.challengesPassed.push(lessonId);
        p.xp += 500;
        // Unlock next lesson
        if (p.currentLesson === lessonId && lessonId < 40) {
            p.currentLesson += 1;
        }
        saveProgress(p);
    }
}

// --- Helper: Lesson Module Status ---

export const getLessonStatus = (lessonId: number) => {
  const p = getProgress();
  const lessonVocab = VOCABULARY.filter(v => v.lessonId === lessonId);
  const masteryTotal = lessonVocab.reduce((acc, v) => acc + (p.vocabMastery[v.id] || 0), 0);
  const avgMastery = lessonVocab.length > 0 ? masteryTotal / lessonVocab.length : 0;
  
  const exercisesCount = p.exercisesCompleted[lessonId] || 0;
  
  const lessonReadings = READINGS.filter(r => r.lessonId === lessonId);
  const readingsDone = lessonReadings.length > 0 && lessonReadings.every(r => p.readingsCompleted.includes(r.id));
  
  const challengePassed = p.challengesPassed.includes(lessonId);

  return {
    grammar: { unlocked: true, completed: p.lessonsCompleted.includes(lessonId) },
    vocab: { 
        unlocked: p.lessonsCompleted.includes(lessonId), 
        mastery: avgMastery,
        completed: avgMastery >= 0.5 
    },
    exercises: { 
        unlocked: avgMastery >= 0.5, 
        count: exercisesCount,
        completed: exercisesCount >= 3 
    },
    reading: { 
        unlocked: exercisesCount >= 3, 
        completed: readingsDone 
    },
    challenge: { 
        unlocked: readingsDone, 
        completed: challengePassed 
    }
  };
};

// --- Recommendation Engine ---

export const getRecommendations = (): Recommendation[] => {
  const p = getProgress();
  const status = getLessonStatus(p.currentLesson);
  const recs: Recommendation[] = [];

  // 1. Grammar
  if (!status.grammar.completed) {
    recs.push({
      id: 'step-1-grammar',
      type: 'lesson',
      message: `Paso 1: Lee la teoría de la Lección ${p.currentLesson}`,
      priority: 'high',
      actionView: AppView.LESSON,
      actionPayload: p.currentLesson
    });
    return recs;
  }

  // 2. Vocab
  if (!status.vocab.completed) {
    recs.push({
      id: 'step-2-vocab',
      type: 'vocab',
      message: `Paso 2: Domina el 50% del vocabulario (${Math.round(status.vocab.mastery * 100)}% actual)`,
      priority: 'high',
      actionView: AppView.SRS
    });
    return recs;
  }

  // 3. Exercises
  if (!status.exercises.completed) {
    recs.push({
      id: 'step-3-ex',
      type: 'exercise',
      message: `Paso 3: Completa 3 sesiones de ejercicios (${status.exercises.count}/3)`,
      priority: 'high',
      actionView: AppView.EXERCISES
    });
    return recs;
  }

  // 4. Reading
  if (!status.reading.completed) {
    recs.push({
      id: 'step-4-read',
      type: 'reading',
      message: `Paso 4: Completa la lectura de la lección`,
      priority: 'high',
      actionView: AppView.READING
    });
    return recs;
  }

  // 5. Challenge
  if (!status.challenge.completed) {
    recs.push({
      id: 'step-5-boss',
      type: 'challenge',
      message: `¡DESAFÍO FINAL! Aprueba el examen para pasar de nivel`,
      priority: 'high',
      actionView: AppView.CHALLENGE,
      actionPayload: p.currentLesson
    });
    return recs;
  }

  return recs;
};