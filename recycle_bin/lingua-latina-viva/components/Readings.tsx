import React, { useState } from 'react';
import { READINGS, completeReading, getProgress, getLessonStatus } from '../services/learningEngine';
import { analyzeLatinText } from '../services/geminiService';
import { MorphAnalysis, AppView } from '../types';
import { Loader2, BookOpen, HelpCircle, Lock } from 'lucide-react';

interface ReadingsProps {
  onBack: () => void;
}

const Readings: React.FC<ReadingsProps> = ({ onBack }) => {
  const progress = getProgress();
  // Show readings for completed lessons OR the current lesson if unlocked
  const currentLessonStatus = getLessonStatus(progress.currentLesson);
  
  const [selectedReading, setSelectedReading] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<MorphAnalysis | null>(null);
  const [analyzingWord, setAnalyzingWord] = useState<string | null>(null);

  const reading = READINGS.find(r => r.id === selectedReading);

  const handleWordClick = async (word: string) => {
    // Clean punctuation
    const cleanWord = word.replace(/[.,;?!]/g, '');
    setAnalyzingWord(cleanWord);
    try {
      const result = await analyzeLatinText(cleanWord);
      if (result && result.length > 0) {
        setAnalysis(result[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setAnalyzingWord(null);
    }
  };

  const handleFinish = () => {
    if (reading) {
        completeReading(reading.id);
        onBack();
    }
  };

  if (!selectedReading) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <h2 className="text-3xl font-display text-roman-red mb-6">Biblioteca</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Show all relevant readings */}
            {READINGS.filter(r => r.lessonId <= progress.currentLesson).map(r => {
                const isCurrentLesson = r.lessonId === progress.currentLesson;
                const isLocked = isCurrentLesson && !currentLessonStatus.reading.unlocked;
                
                return (
                    <div 
                        key={r.id} 
                        onClick={!isLocked ? () => setSelectedReading(r.id) : undefined}
                        className={`bg-white p-6 rounded-lg shadow-md border border-gray-200 transition relative overflow-hidden ${isLocked ? 'cursor-not-allowed opacity-75' : 'cursor-pointer hover:border-roman-gold'}`}
                    >
                        {isLocked && (
                            <div className="absolute inset-0 bg-gray-50/80 flex flex-col items-center justify-center z-10 text-center p-4">
                                <Lock className="h-8 w-8 text-gray-400 mb-2" />
                                <span className="text-xs font-bold text-gray-500 uppercase">Bloqueado</span>
                                <p className="text-xs text-gray-400 mt-1">Completa 3 sesiones de ejercicios para desbloquear.</p>
                            </div>
                        )}
                        <div className="flex justify-between items-center mb-2">
                            <h3 className="font-serif font-bold text-xl text-gray-900">{r.title}</h3>
                            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">Lección {r.lessonId}</span>
                        </div>
                        <p className="text-gray-500 text-sm line-clamp-2">{r.content}</p>
                    </div>
                );
            })}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 flex flex-col lg:flex-row gap-6">
      {/* Text Area */}
      <div className="flex-1">
        <div className="bg-white p-8 rounded-lg shadow-lg border-t-4 border-roman-red min-h-[500px]">
          <h2 className="text-3xl font-display text-center mb-8 text-roman-black">{reading?.title}</h2>
          <div className="font-serif text-2xl leading-loose text-justify text-gray-800">
            {reading?.content.split(' ').map((word, idx) => (
              <span 
                key={idx} 
                onClick={() => handleWordClick(word)}
                className="cursor-pointer hover:bg-yellow-100 hover:text-roman-red hover:text-white rounded px-1 transition"
              >
                {word}{' '}
              </span>
            ))}
          </div>
          
          <div className="mt-12 p-6 bg-roman-stone rounded-lg text-gray-800">
            <h3 className="font-bold mb-4 flex items-center gap-2 text-roman-black"><HelpCircle className="h-5 w-5"/> Comprensión</h3>
            <div className="space-y-4">
                {reading?.questions.map((q, i) => (
                    <div key={i}>
                        <p className="font-bold text-sm text-gray-900">{q.question}</p>
                        <p className="text-gray-600 text-sm italic">{q.answer}</p>
                    </div>
                ))}
            </div>
          </div>

          <button onClick={handleFinish} className="mt-8 w-full bg-roman-gold text-white py-3 rounded font-bold hover:bg-yellow-600 transition">
            Terminar Lectura
          </button>
        </div>
      </div>

      {/* Sidebar Analysis */}
      <div className="w-full lg:w-80 shrink-0">
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200 sticky top-6">
          <h3 className="font-display font-bold text-lg mb-4 text-roman-red border-b pb-2">Análisis Instantáneo</h3>
          
          {analyzingWord ? (
            <div className="flex items-center gap-2 text-gray-500 py-10 justify-center">
                <Loader2 className="animate-spin"/> Analizando...
            </div>
          ) : analysis ? (
            <div className="space-y-3">
              <div>
                <span className="text-xs text-gray-400 uppercase">Palabra</span>
                <p className="text-2xl font-serif text-roman-black">{analysis.word}</p>
              </div>
              <div>
                <span className="text-xs text-gray-400 uppercase">Lema</span>
                <p className="text-lg italic text-gray-800">{analysis.lemma}</p>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                    <span className="text-xs text-gray-400 uppercase">POS</span>
                    <p className="text-sm font-medium text-gray-800">{analysis.pos}</p>
                </div>
                <div>
                    <span className="text-xs text-gray-400 uppercase">Función</span>
                    <p className="text-sm text-blue-600">{analysis.dependency || 'N/A'}</p>
                </div>
              </div>
              <div>
                <span className="text-xs text-gray-400 uppercase">Morfología</span>
                <p className="text-sm bg-gray-50 text-gray-800 p-2 rounded">{analysis.morphology}</p>
              </div>
              <div>
                <span className="text-xs text-gray-400 uppercase">Traducción</span>
                <p className="text-lg text-roman-red">{analysis.translation}</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-400 text-sm italic text-center py-10">
                Haz clic en cualquier palabra del texto para ver su análisis morfológico y sintáctico.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Readings;