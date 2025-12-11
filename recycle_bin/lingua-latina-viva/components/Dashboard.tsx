import React, { useEffect, useState } from 'react';
import { AppView, Recommendation, UserProgress } from '../types';
import { getProgress, getRecommendations, getLessonStatus, LESSONS } from '../services/learningEngine';
import { Play, Star, BookOpen, Brain, TrendingUp, Lock, CheckCircle, Trophy, ArrowRight } from 'lucide-react';

interface DashboardProps {
  changeView: (view: AppView, payload?: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ changeView }) => {
  const [progress, setProgress] = useState<UserProgress | null>(null);
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [currentStatus, setCurrentStatus] = useState<any>(null);

  useEffect(() => {
    const p = getProgress();
    setProgress(p);
    setRecs(getRecommendations());
    setCurrentStatus(getLessonStatus(p.currentLesson));
  }, []);

  if (!progress || !currentStatus) return <div className="p-8 text-center text-gray-500">Cargando ecosistema...</div>;

  const currentLessonData = LESSONS.find(l => l.id === progress.currentLesson);

  const StepCard = ({ title, status, icon: Icon, onClick, description, isLocked }: any) => (
    <div 
        onClick={!isLocked ? onClick : undefined}
        className={`relative p-5 rounded-xl border-2 transition-all duration-300 flex flex-col items-center text-center gap-3 ${
        isLocked 
            ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed' 
            : status.completed 
                ? 'bg-green-50 border-green-200 cursor-pointer hover:shadow-md'
                : 'bg-white border-roman-gold shadow-lg transform hover:-translate-y-1 cursor-pointer'
    }`}>
        {status.completed && (
            <div className="absolute top-2 right-2 text-green-500">
                <CheckCircle className="h-5 w-5" />
            </div>
        )}
        {isLocked && (
             <div className="absolute top-2 right-2 text-gray-400">
                <Lock className="h-4 w-4" />
            </div>
        )}
        <div className={`p-3 rounded-full ${isLocked ? 'bg-gray-100' : status.completed ? 'bg-green-100 text-green-700' : 'bg-roman-stone text-roman-red'}`}>
            <Icon className="h-6 w-6" />
        </div>
        <div>
            <h4 className="font-bold font-display text-sm uppercase">{title}</h4>
            <p className="text-xs text-gray-500 mt-1">{description}</p>
        </div>
    </div>
  );

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-12">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-end border-b border-gray-200 pb-6">
        <div>
            <span className="text-roman-gold font-bold uppercase tracking-widest text-xs mb-2 block">Tu Progreso Actual</span>
            <h1 className="text-4xl font-display text-roman-black">Lección {progress.currentLesson}: {currentLessonData?.title}</h1>
        </div>
        <div className="flex gap-4 mt-4 md:mt-0">
             <div className="text-right">
                <div className="text-2xl font-bold text-roman-red">{progress.xp}</div>
                <div className="text-xs text-gray-500 uppercase">XP Total</div>
             </div>
        </div>
      </div>

      {/* The Cycle (Main Action Area) */}
      <section>
        <h3 className="text-xl font-display text-gray-800 mb-6 flex items-center gap-2">
           <Play className="h-5 w-5 text-roman-red" /> Ciclo de Aprendizaje
        </h3>
        
        {/* Visual Progress Bar */}
        <div className="w-full bg-gray-200 h-2 rounded-full mb-8 overflow-hidden flex">
             <div className={`h-full bg-green-500 transition-all duration-1000`} style={{width: currentStatus.grammar.completed ? '20%' : '0%'}}></div>
             <div className={`h-full bg-green-500 transition-all duration-1000 border-l border-white/20`} style={{width: currentStatus.vocab.completed ? '20%' : '0%'}}></div>
             <div className={`h-full bg-green-500 transition-all duration-1000 border-l border-white/20`} style={{width: currentStatus.exercises.completed ? '20%' : '0%'}}></div>
             <div className={`h-full bg-green-500 transition-all duration-1000 border-l border-white/20`} style={{width: currentStatus.reading.completed ? '20%' : '0%'}}></div>
             <div className={`h-full bg-green-500 transition-all duration-1000 border-l border-white/20`} style={{width: currentStatus.challenge.completed ? '20%' : '0%'}}></div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <StepCard 
                title="1. Gramática" 
                icon={BookOpen} 
                status={currentStatus.grammar}
                isLocked={false}
                description="Lee la teoría"
                onClick={() => changeView(AppView.LESSON, progress.currentLesson)}
            />
            <StepCard 
                title="2. Vocabulario" 
                icon={Brain} 
                status={currentStatus.vocab}
                isLocked={!currentStatus.vocab.unlocked}
                description="Domina 50%"
                onClick={() => changeView(AppView.SRS)}
            />
            <StepCard 
                title="3. Ejercicios" 
                icon={TrendingUp} 
                status={currentStatus.exercises}
                isLocked={!currentStatus.exercises.unlocked}
                description="3 sesiones"
                onClick={() => changeView(AppView.EXERCISES)}
            />
            <StepCard 
                title="4. Lectura" 
                icon={BookOpen} 
                status={currentStatus.reading}
                isLocked={!currentStatus.reading.unlocked}
                description="Aplica lo aprendido"
                onClick={() => changeView(AppView.READING)}
            />
            <StepCard 
                title="5. Desafío" 
                icon={Trophy} 
                status={currentStatus.challenge}
                isLocked={!currentStatus.challenge.unlocked}
                description="Prueba final"
                onClick={() => changeView(AppView.CHALLENGE, progress.currentLesson)}
            />
        </div>
      </section>

      {/* Recommendations Banner */}
      {recs.length > 0 && (
        <section className="bg-roman-stone border-l-4 border-roman-red p-6 rounded-r-lg shadow-sm flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <h4 className="font-bold text-roman-red uppercase text-sm mb-1">Siguiente Paso Recomendado</h4>
                <p className="font-serif text-lg text-gray-800">{recs[0].message}</p>
            </div>
            <button 
                onClick={() => changeView(recs[0].actionView, recs[0].actionPayload)}
                className="bg-roman-red text-white px-6 py-3 rounded-full font-bold hover:bg-red-900 transition flex items-center gap-2 shadow-md"
            >
                Continuar <ArrowRight className="h-4 w-4" />
            </button>
        </section>
      )}

       {/* Map of Past Lessons */}
       <section className="pt-8 border-t border-gray-200">
         <h3 className="text-gray-400 font-bold uppercase text-xs mb-4">Mapa de Progreso</h3>
         <div className="flex gap-4 overflow-x-auto pb-4">
            {LESSONS.map(l => (
                <div key={l.id} className={`flex-shrink-0 w-48 p-4 rounded-lg border ${
                    l.id < progress.currentLesson 
                        ? 'bg-green-50 border-green-200 opacity-75' 
                        : l.id === progress.currentLesson
                            ? 'bg-white border-roman-gold ring-2 ring-roman-gold ring-offset-2'
                            : 'bg-gray-50 border-gray-200 grayscale opacity-50'
                }`}>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs font-bold text-gray-500">LECCIÓN {l.id}</span>
                        {l.id < progress.currentLesson && <CheckCircle className="h-4 w-4 text-green-500" />}
                    </div>
                    <h4 className="font-serif font-bold text-sm truncate">{l.title}</h4>
                </div>
            ))}
         </div>
       </section>

    </div>
  );
};

export default Dashboard;