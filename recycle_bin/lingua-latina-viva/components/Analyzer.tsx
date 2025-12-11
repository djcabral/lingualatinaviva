import React, { useState } from 'react';
import { analyzeLatinText } from '../services/geminiService';
import { MorphAnalysis } from '../types';
import { Search, Loader2, Info, ArrowUpRight, GitCommit } from 'lucide-react';

const Analyzer: React.FC = () => {
  const [input, setInput] = useState('');
  const [analysis, setAnalysis] = useState<MorphAnalysis[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedWordId, setSelectedWordId] = useState<number | null>(null);

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError('');
    setAnalysis(null);
    setSelectedWordId(null);
    try {
      const result = await analyzeLatinText(input);
      setAnalysis(result);
    } catch (e) {
      setError("Error al analizar el texto. Por favor verifique su conexión o intente con un texto más corto.");
    } finally {
      setLoading(false);
    }
  };

  const selectedWord = analysis?.find(w => w.id === selectedWordId);
  const headWord = selectedWord && selectedWord.headId !== 0 ? analysis?.find(w => w.id === selectedWord.headId) : null;
  const dependentWords = selectedWord ? analysis?.filter(w => w.headId === selectedWord.id) : [];

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-display text-roman-red mb-2">Laboratorio Sintáctico</h2>
        <p className="text-gray-600">Introduce un texto para visualizar su estructura gramatical profunda.</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 border-t-4 border-roman-gold mb-8">
        <div className="relative">
          <textarea
            className="w-full p-4 border border-gray-300 rounded-md font-serif text-xl focus:ring-2 focus:ring-roman-red focus:border-transparent outline-none transition bg-white text-gray-900 resize-none"
            rows={3}
            placeholder="Ej: Puella pulchra rosam dat..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !input.trim()}
            className="absolute bottom-4 right-4 bg-roman-red text-white px-6 py-2 rounded-full hover:bg-red-900 transition disabled:opacity-50 font-bold flex items-center gap-2 shadow-lg"
          >
            {loading ? <Loader2 className="animate-spin h-5 w-5" /> : <Search className="h-5 w-5" />}
            {loading ? 'Analizando...' : 'Analizar'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 border border-red-200 rounded-md mb-8">
          {error}
        </div>
      )}

      {analysis && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Visual Interaction */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Sentence Viewer */}
            <div className="bg-white p-8 rounded-lg shadow-md border border-gray-200">
                <h3 className="text-xs font-bold text-gray-400 uppercase mb-4 tracking-widest">Estructura de la Oración (Haz clic en una palabra)</h3>
                <div className="flex flex-wrap gap-3 leading-loose">
                    {analysis.map((item) => {
                        const isSelected = selectedWordId === item.id;
                        const isHead = selectedWord && item.id === selectedWord.headId;
                        const isDependent = selectedWord && item.headId === selectedWord.id;

                        let borderClass = "border-gray-200 hover:border-roman-gold";
                        let bgClass = "bg-white";
                        let textClass = "text-gray-800";
                        let badge = null;

                        if (isSelected) {
                            borderClass = "border-roman-red ring-2 ring-roman-red ring-opacity-50";
                            bgClass = "bg-red-50";
                            textClass = "text-roman-red font-bold";
                        } else if (isHead) {
                            borderClass = "border-roman-gold border-dashed";
                            bgClass = "bg-yellow-50";
                            textClass = "text-yellow-800";
                            badge = <span className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-roman-gold text-white text-[10px] px-1 rounded">Regente</span>;
                        } else if (isDependent) {
                            borderClass = "border-blue-300 border-dashed";
                            bgClass = "bg-blue-50";
                            textClass = "text-blue-800";
                        }

                        return (
                            <div 
                                key={item.id}
                                onClick={() => setSelectedWordId(item.id)}
                                className={`relative cursor-pointer px-4 py-2 rounded-lg border-2 transition-all duration-200 ${borderClass} ${bgClass}`}
                            >
                                {badge}
                                <span className={`font-serif text-xl ${textClass}`}>{item.word}</span>
                                <div className="text-[10px] text-center text-gray-400 mt-1 uppercase font-sans tracking-tight">{item.dependency}</div>
                            </div>
                        );
                    })}
                </div>
                
                <div className="mt-6 flex gap-4 text-xs text-gray-500 justify-end">
                    <div className="flex items-center gap-1"><div className="w-3 h-3 bg-red-50 border border-roman-red rounded"></div> Seleccionada</div>
                    <div className="flex items-center gap-1"><div className="w-3 h-3 bg-yellow-50 border border-roman-gold border-dashed rounded"></div> Regente (Padre)</div>
                    <div className="flex items-center gap-1"><div className="w-3 h-3 bg-blue-50 border border-blue-300 border-dashed rounded"></div> Dependiente (Hijo)</div>
                </div>
            </div>

            {/* Detailed Table */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <table className="w-full text-left text-sm">
                    <thead className="bg-roman-stone text-gray-600 font-display">
                        <tr>
                            <th className="p-3">Palabra</th>
                            <th className="p-3">Lema</th>
                            <th className="p-3">Morfología</th>
                            <th className="p-3">Función</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {analysis.map(item => (
                            <tr 
                                key={item.id} 
                                onClick={() => setSelectedWordId(item.id)}
                                className={`cursor-pointer hover:bg-gray-50 transition ${selectedWordId === item.id ? 'bg-red-50 hover:bg-red-50' : ''}`}
                            >
                                <td className="p-3 font-serif font-bold text-gray-800">{item.word}</td>
                                <td className="p-3 text-gray-500 italic">{item.lemma}</td>
                                <td className="p-3 text-gray-600">{item.morphology}</td>
                                <td className="p-3 text-roman-red font-medium">{item.dependency}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

          </div>

          {/* Right Column: Pedagogical Insight */}
          <div className="lg:col-span-1">
             <div className="sticky top-6">
                {selectedWord ? (
                    <div className="bg-white p-6 rounded-lg shadow-lg border-t-4 border-roman-red animate-fade-in">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="text-3xl font-serif text-roman-black">{selectedWord.word}</h3>
                                <p className="text-gray-500 italic text-lg">{selectedWord.lemma}</p>
                            </div>
                            <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs uppercase font-bold tracking-wider">{selectedWord.pos}</span>
                        </div>

                        <div className="mb-6">
                            <h4 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                                <Info className="h-4 w-4 text-roman-gold" /> Análisis Sintáctico
                            </h4>
                            <div className="bg-roman-stone p-4 rounded-lg text-gray-700">
                                <p className="font-bold text-roman-red text-lg mb-1">{selectedWord.dependency}</p>
                                <p className="text-sm leading-relaxed">{selectedWord.explanation}</p>
                            </div>
                        </div>

                        <div className="space-y-4 text-sm">
                            <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                                <span className="text-gray-400">Traducción</span>
                                <span className="font-medium text-gray-800">{selectedWord.translation}</span>
                            </div>
                            <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                                <span className="text-gray-400">Morfología</span>
                                <span className="font-medium text-gray-800">{selectedWord.morphology}</span>
                            </div>
                            <div className="flex items-center justify-between pt-2">
                                <span className="text-gray-400 flex items-center gap-1"><ArrowUpRight className="h-3 w-3"/> Depende de</span>
                                <span className="font-medium text-blue-600 cursor-pointer hover:underline" onClick={() => headWord && setSelectedWordId(headWord.id)}>
                                    {headWord ? headWord.word : 'RAÍZ'}
                                </span>
                            </div>
                        </div>

                    </div>
                ) : (
                    <div className="bg-gray-50 border-2 border-dashed border-gray-200 rounded-lg p-8 text-center text-gray-400">
                        <GitCommit className="h-12 w-12 mx-auto mb-4 opacity-50" />
                        <p>Selecciona una palabra para ver su ficha pedagógica detallada y sus relaciones.</p>
                    </div>
                )}
             </div>
          </div>

        </div>
      )}
    </div>
  );
};

export default Analyzer;