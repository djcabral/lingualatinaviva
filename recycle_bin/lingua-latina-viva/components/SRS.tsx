import React, { useState, useEffect } from 'react';
import { Flashcard } from '../types';
import { VOCABULARY, getProgress, updateVocabMastery, getLessonStatus } from '../services/learningEngine';
import { RotateCcw, CheckCircle, XCircle, Brain, ArrowLeft, Lock } from 'lucide-react';

const SRS: React.FC = () => {
  const [deck, setDeck] = useState<Flashcard[]>([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [progress, setProgress] = useState(getProgress());

  useEffect(() => {
    // Filter specifically for CURRENT lesson to focus study
    const p = getProgress();
    setProgress(p);
    const activeDeck = VOCABULARY.filter(card => card.lessonId === p.currentLesson);
    setDeck(activeDeck);
  }, []);

  const currentCard = deck[currentCardIndex];
  const lessonStatus = getLessonStatus(progress.currentLesson);
  const masteryPct = Math.round(lessonStatus.vocab.mastery * 100);

  const handleNext = (rating: 'hard' | 'good' | 'easy') => {
    const success = rating === 'good' || rating === 'easy';
    updateVocabMastery(currentCard.id, success);
    // Refresh progress for UI
    setProgress(getProgress());

    setIsFlipped(false);
    setTimeout(() => {
      if (currentCardIndex < deck.length - 1) {
        setCurrentCardIndex(prev => prev + 1);
      } else {
        setSessionComplete(true);
      }
    }, 200);
  };

  const resetSession = () => {
    setSessionComplete(false);
    setCurrentCardIndex(0);
    setIsFlipped(false);
  };

  if (deck.length === 0) {
    return (
        <div className="flex flex-col items-center justify-center h-96 p-6 text-center">
            <Lock className="h-12 w-12 text-gray-300 mb-4" />
            <p className="text-gray-500">Primero lee la Lección {progress.currentLesson} para desbloquear este vocabulario.</p>
        </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      
      {/* Context Header */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-100">
         <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold text-gray-500 uppercase">Vocabulario Lección {progress.currentLesson}</span>
            <span className="text-xs font-bold text-roman-red">{masteryPct}% Dominado</span>
         </div>
         <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
            <div className="bg-roman-gold h-full transition-all duration-500" style={{ width: `${masteryPct}%` }}></div>
         </div>
         <p className="text-xs text-gray-400 mt-2 text-center">
            {masteryPct < 50 
                ? `Necesitas llegar al 50% para desbloquear Ejercicios` 
                : `¡Excelente! Ejercicios desbloqueados.`}
         </p>
      </div>

      {!sessionComplete ? (
        <>
            <div 
                className="h-80 w-full cursor-pointer group" 
                style={{ perspective: '1000px' }}
                onClick={() => setIsFlipped(!isFlipped)}
            >
                <div 
                    className="relative w-full h-full duration-500 transition-all"
                    style={{ 
                        transformStyle: 'preserve-3d', 
                        transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)' 
                    }}
                >
                
                {/* Front (Latin) */}
                <div 
                    className="absolute w-full h-full bg-white border-2 border-roman-gold rounded-xl shadow-lg p-8 flex flex-col items-center justify-center"
                    style={{ backfaceVisibility: 'hidden' }}
                >
                    <span className="text-sm uppercase tracking-widest text-gray-400 mb-4 font-sans">{currentCard.partOfSpeech}</span>
                    <h3 className="text-5xl font-serif text-roman-black">{currentCard.latin}</h3>
                    <p className="mt-8 text-gray-400 text-sm italic">Haz clic para voltear</p>
                </div>

                {/* Back (Spanish) */}
                <div 
                    className="absolute w-full h-full bg-roman-black border-2 border-roman-black rounded-xl shadow-lg p-8 flex flex-col items-center justify-center"
                    style={{ 
                        backfaceVisibility: 'hidden', 
                        transform: 'rotateY(180deg)' 
                    }}
                >
                    <span className="text-sm uppercase tracking-widest text-gray-400 mb-4 font-sans">Traducción</span>
                    <h3 className="text-4xl font-serif text-white">{currentCard.spanish}</h3>
                </div>
                </div>
            </div>

            <div className={`mt-8 flex justify-center gap-4 transition-opacity duration-300 ${isFlipped ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
                <button onClick={() => handleNext('hard')} className="flex flex-col items-center gap-1 p-3 rounded-lg hover:bg-red-100 transition w-24">
                <XCircle className="text-red-600 h-8 w-8" />
                <span className="text-xs font-bold text-red-700">Difícil</span>
                </button>
                <button onClick={() => handleNext('good')} className="flex flex-col items-center gap-1 p-3 rounded-lg hover:bg-yellow-100 transition w-24">
                <RotateCcw className="text-yellow-600 h-8 w-8" />
                <span className="text-xs font-bold text-yellow-700">Bien</span>
                </button>
                <button onClick={() => handleNext('easy')} className="flex flex-col items-center gap-1 p-3 rounded-lg hover:bg-green-100 transition w-24">
                <CheckCircle className="text-green-600 h-8 w-8" />
                <span className="text-xs font-bold text-green-700">Fácil</span>
                </button>
            </div>
            <div className="text-center mt-6 text-sm text-gray-400">
                Tarjeta {currentCardIndex + 1} de {deck.length}
            </div>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center h-80 p-6 text-center bg-white rounded-xl shadow-lg border border-gray-100">
            <Brain className="h-16 w-16 text-roman-gold mb-4" />
            <h2 className="text-2xl font-display text-roman-black mb-2">¡Sesión Completada!</h2>
            <p className="text-gray-600 mb-6">Tu dominio del vocabulario ha aumentado.</p>
            <button 
            onClick={resetSession}
            className="px-6 py-2 bg-roman-red text-white rounded-md hover:bg-red-900 transition"
            >
            Repasar de nuevo
            </button>
        </div>
      )}
    </div>
  );
};

export default SRS;