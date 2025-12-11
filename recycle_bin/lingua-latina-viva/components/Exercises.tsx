import React, { useState } from 'react';
import { generateLatinQuiz } from '../services/geminiService';
import { ExerciseDifficulty, QuizQuestion } from '../types';
import { getProgress, incrementExerciseCount, LESSONS, getLessonStatus } from '../services/learningEngine';
import { GraduationCap, ArrowRight, Check, X, RefreshCw, Lock } from 'lucide-react';

const Exercises: React.FC = () => {
  const [step, setStep] = useState<'config' | 'quiz' | 'results'>('config');
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState<ExerciseDifficulty>(ExerciseDifficulty.BEGINNER);
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [score, setScore] = useState(0);

  const progress = getProgress();
  const currentLesson = LESSONS.find(l => l.id === progress.currentLesson);
  const lessonStatus = getLessonStatus(progress.currentLesson);

  // Auto-select current lesson topic
  if (!topic && currentLesson) {
      setTopic(currentLesson.title);
  }

  const startQuiz = async () => {
    setLoading(true);
    try {
      const qs = await generateLatinQuiz(difficulty, topic);
      setQuestions(qs);
      setStep('quiz');
      setAnswers({});
    } catch (error) {
      alert("Error generando ejercicios. Intente de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (qIdx: number, option: string) => {
    setAnswers(prev => ({ ...prev, [qIdx]: option }));
  };

  const submitQuiz = () => {
    let newScore = 0;
    questions.forEach((q, idx) => {
      if (answers[idx] === q.correctAnswer) {
        newScore++;
      }
    });
    setScore(newScore);
    
    // Register progress in the engine
    if (currentLesson) {
        incrementExerciseCount(currentLesson.id, newScore);
    }

    setStep('results');
  };

  const reset = () => {
    setStep('config');
    setQuestions([]);
    setScore(0);
  };

  // 1. Check if Locked
  if (!lessonStatus.exercises.unlocked) {
      return (
        <div className="flex flex-col items-center justify-center h-96 text-center p-6 max-w-lg mx-auto">
            <div className="bg-gray-100 p-6 rounded-full mb-6">
                <Lock className="h-12 w-12 text-gray-400" />
            </div>
            <h2 className="text-2xl font-display text-gray-700 mb-2">Ejercicios Bloqueados</h2>
            <p className="text-gray-500 mb-6">
                Debes dominar al menos el <strong className="text-roman-red">50% del vocabulario</strong> de la Lección {progress.currentLesson} antes de practicar gramática.
            </p>
            <div className="w-full bg-gray-200 h-4 rounded-full overflow-hidden mb-2">
                <div className="bg-gray-400 h-full" style={{width: `${lessonStatus.vocab.mastery * 100}%`}}></div>
            </div>
            <span className="text-xs text-gray-400">Progreso actual: {Math.round(lessonStatus.vocab.mastery * 100)}%</span>
        </div>
      )
  }

  if (step === 'config') {
    return (
      <div className="max-w-2xl mx-auto p-6">
        
        {/* Progress Header */}
        <div className="mb-8 bg-white p-4 rounded-lg shadow-sm border border-gray-100 flex items-center justify-between">
            <div>
                <h3 className="text-sm font-bold text-gray-500 uppercase">Meta de Práctica</h3>
                <p className="text-xs text-gray-400">Completa 3 sesiones para desbloquear la Lectura</p>
            </div>
            <div className="flex gap-1">
                {[1, 2, 3].map(i => (
                    <div key={i} className={`w-8 h-2 rounded-full ${i <= lessonStatus.exercises.count ? 'bg-green-500' : 'bg-gray-200'}`}></div>
                ))}
            </div>
        </div>

        <h2 className="text-3xl font-display text-roman-red mb-6 flex items-center gap-3">
          <GraduationCap /> Práctica: {currentLesson?.title}
        </h2>
        
        <div className="bg-white p-8 rounded-lg shadow-md border-t-4 border-roman-red">
          <div className="mb-8">
            <label className="block text-gray-700 font-bold mb-2">Dificultad</label>
            <div className="grid grid-cols-3 gap-4">
              {Object.values(ExerciseDifficulty).map((diff) => (
                <button
                  key={diff}
                  onClick={() => setDifficulty(diff)}
                  className={`py-3 rounded-md font-medium transition ${
                    difficulty === diff 
                      ? 'bg-roman-black text-white' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={startQuiz}
            disabled={loading}
            className="w-full bg-roman-red text-white py-4 rounded-md font-bold text-lg hover:bg-red-900 transition flex justify-center items-center gap-2"
          >
            {loading ? <RefreshCw className="animate-spin" /> : 'Generar Ejercicios con IA'}
          </button>
        </div>
      </div>
    );
  }

  if (step === 'quiz') {
    return (
      <div className="max-w-3xl mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-gray-700">{topic} - {difficulty}</h3>
          <span className="text-sm bg-roman-gold text-white px-3 py-1 rounded-full">
            {Object.keys(answers).length}/{questions.length} Respondidas
          </span>
        </div>

        <div className="space-y-8">
          {questions.map((q, idx) => (
            <div key={idx} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <p className="font-serif text-lg mb-4 text-roman-black">{q.question}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {q.options.map((opt) => (
                  <button
                    key={opt}
                    onClick={() => handleSelectAnswer(idx, opt)}
                    className={`text-left p-3 rounded-md border transition ${
                      answers[idx] === opt
                        ? 'border-roman-red bg-red-50 text-roman-red font-medium'
                        : 'border-gray-200 hover:border-gray-400'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex justify-end">
          <button
            onClick={submitQuiz}
            disabled={Object.keys(answers).length !== questions.length}
            className="bg-roman-black text-white px-8 py-3 rounded-md hover:bg-gray-800 disabled:opacity-50 transition font-bold flex items-center gap-2"
          >
            Finalizar <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6 text-center">
      <h2 className="text-4xl font-display text-roman-black mb-2">Resultados</h2>
      <p className="text-xl text-gray-600 mb-8">Has obtenido <span className="font-bold text-roman-red">{score}</span> de <span className="font-bold">{questions.length}</span> aciertos.</p>

      <div className="space-y-6 text-left mb-10">
        {questions.map((q, idx) => (
          <div key={idx} className={`p-4 rounded-lg border ${answers[idx] === q.correctAnswer ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
            <p className="font-serif font-bold text-gray-800 mb-2">{q.question}</p>
            <div className="flex items-center gap-2 mb-1">
              {answers[idx] === q.correctAnswer ? <Check className="text-green-600 h-4 w-4" /> : <X className="text-red-600 h-4 w-4" />}
              <span className="text-sm">Tu respuesta: <strong>{answers[idx]}</strong></span>
            </div>
            {answers[idx] !== q.correctAnswer && (
               <div className="text-sm text-green-700 mb-2">Correcta: <strong>{q.correctAnswer}</strong></div>
            )}
            <div className="text-xs text-gray-500 italic border-t border-gray-200 pt-2 mt-2">
              Nota: {q.explanation}
            </div>
          </div>
        ))}
      </div>

      <button onClick={reset} className="bg-roman-gold text-white px-8 py-3 rounded-md hover:bg-yellow-600 font-bold">
        Nueva Sesión
      </button>
    </div>
  );
};

export default Exercises;