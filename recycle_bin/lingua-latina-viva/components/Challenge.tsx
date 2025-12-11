import React, { useState } from 'react';
import { CHALLENGES, passChallenge, getLessonStatus } from '../services/learningEngine';
import { ArrowLeft, Trophy, CheckCircle, XCircle, Lock } from 'lucide-react';
import confetti from 'https://esm.sh/canvas-confetti@1.6.0';

interface ChallengeProps {
  lessonId: number;
  onBack: () => void;
}

const Challenge: React.FC<ChallengeProps> = ({ lessonId, onBack }) => {
  const challenge = CHALLENGES.find(c => c.lessonId === lessonId);
  const status = getLessonStatus(lessonId);

  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [completed, setCompleted] = useState(false);
  const [passed, setPassed] = useState(false);
  const [score, setScore] = useState(0);

  // 1. Check Locks
  if (!status.challenge.unlocked) {
      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-8">
            <div className="bg-gray-100 p-8 rounded-full mb-6">
                <Lock className="h-16 w-16 text-gray-400" />
            </div>
            <h2 className="text-3xl font-display text-gray-600 mb-4">Desafío Bloqueado</h2>
            <p className="text-gray-500 max-w-md">
                Debes completar la <strong>Lectura</strong> de esta lección antes de intentar el desafío final.
            </p>
            <button onClick={onBack} className="mt-8 text-roman-red font-bold underline">Volver al mapa</button>
        </div>
      );
  }

  if (!challenge) return <div>Desafío no encontrado.</div>;

  const handleAnswer = (option: string) => {
    const newAnswers = [...answers, option];
    setAnswers(newAnswers);

    if (currentQ < challenge.questions.length - 1) {
        setCurrentQ(currentQ + 1);
    } else {
        finish(newAnswers);
    }
  };

  const finish = (finalAnswers: string[]) => {
    let correct = 0;
    challenge.questions.forEach((q, i) => {
        if (q.correctAnswer === finalAnswers[i]) correct++;
    });
    
    const finalScore = correct / challenge.questions.length;
    setScore(finalScore);
    setCompleted(true);
    
    if (finalScore >= 0.8) {
        setPassed(true);
        passChallenge(lessonId);
        confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
  };

  if (completed) {
      return (
        <div className="max-w-2xl mx-auto p-8 text-center bg-white rounded-lg shadow-xl mt-10">
            {passed ? (
                <>
                    <div className="mx-auto w-24 h-24 bg-yellow-100 rounded-full flex items-center justify-center mb-6">
                        <Trophy className="h-12 w-12 text-yellow-600" />
                    </div>
                    <h2 className="text-4xl font-display text-roman-red mb-4">¡Victoria!</h2>
                    <p className="text-xl text-gray-600 mb-8">Has dominado la Lección {lessonId}.</p>
                    <div className="text-5xl font-bold text-gray-800 mb-8">{Math.round(score * 100)}%</div>
                    <p className="text-sm text-gray-400 mb-8">Has desbloqueado el siguiente nivel.</p>
                    <button onClick={onBack} className="bg-roman-red text-white px-8 py-4 rounded-full font-bold shadow-lg hover:bg-red-900 transition">
                        Continuar Aprendizaje
                    </button>
                </>
            ) : (
                <>
                    <div className="mx-auto w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mb-6">
                        <XCircle className="h-12 w-12 text-red-600" />
                    </div>
                    <h2 className="text-3xl font-display text-gray-700 mb-4">Intento Fallido</h2>
                    <p className="text-gray-600 mb-8">Necesitas un 80% para aprobar. Tu nota: {Math.round(score * 100)}%</p>
                    <button onClick={() => window.location.reload()} className="bg-roman-black text-white px-8 py-3 rounded-md font-bold hover:bg-gray-800 transition">
                        Intentar de Nuevo
                    </button>
                </>
            )}
        </div>
      )
  }

  const q = challenge.questions[currentQ];

  return (
    <div className="max-w-3xl mx-auto p-6 min-h-screen flex flex-col">
        <div className="flex justify-between items-center mb-8">
            <button onClick={onBack} className="text-gray-400 hover:text-gray-600 transition-colors"><ArrowLeft /></button>
            <span className="text-sm font-bold text-roman-red uppercase tracking-widest">Desafío Final • Lección {lessonId}</span>
            <div className="w-8"></div>
        </div>

        <div className="w-full bg-gray-200 h-2 rounded-full mb-8">
            <div className="bg-roman-red h-full transition-all" style={{width: `${(currentQ / challenge.questions.length) * 100}%`}}></div>
        </div>

        <div className="flex-1 flex flex-col justify-center">
            <h2 className="text-2xl md:text-3xl font-serif text-center mb-12 leading-relaxed text-gray-900">
                {q.question}
            </h2>

            <div className="grid grid-cols-1 gap-4">
                {q.options.map((opt) => (
                    <button 
                        key={opt}
                        onClick={() => handleAnswer(opt)}
                        className="p-5 text-lg border-2 border-gray-100 rounded-xl bg-white hover:border-roman-gold hover:bg-yellow-50 transition text-left font-serif text-gray-800 shadow-sm"
                    >
                        {opt}
                    </button>
                ))}
            </div>
        </div>
    </div>
  );
};

export default Challenge;