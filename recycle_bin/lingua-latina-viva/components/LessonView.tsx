import React from 'react';
import { LESSONS, completeLesson } from '../services/learningEngine';
import { ArrowLeft, CheckCircle } from 'lucide-react';

interface LessonViewProps {
  lessonId: number;
  onBack: () => void;
  onComplete: () => void;
}

const LessonView: React.FC<LessonViewProps> = ({ lessonId, onBack, onComplete }) => {
  const lesson = LESSONS.find(l => l.id === lessonId);

  if (!lesson) return <div>Lección no encontrada</div>;

  const handleFinish = () => {
    completeLesson(lessonId);
    onComplete();
  };

  // Helper to parse **bold** text
  const parseInline = (text: string) => {
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-bold text-roman-red">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  // Helper to render markdown-like content (Headers, Tables, Paragraphs)
  const renderContent = (content: string) => {
    const lines = content.split('\n');
    const nodes: React.ReactNode[] = [];
    let tableBuffer: string[] = [];

    const flushTable = (keyIndex: number) => {
      if (tableBuffer.length === 0) return;

      // Extract headers
      const headers = tableBuffer[0].split('|').filter(c => c.trim()).map(c => c.trim());
      
      // Determine where data rows start (skip separator line like |---|---|)
      let startIndex = 1;
      if (tableBuffer.length > 1 && tableBuffer[1].includes('---')) {
        startIndex = 2;
      }
      
      const rows = tableBuffer.slice(startIndex).map(row => 
        row.split('|').filter(c => c.trim()).map(c => c.trim())
      );

      nodes.push(
        <div key={`table-${keyIndex}`} className="overflow-x-auto my-6">
          <table className="min-w-full border-collapse border border-gray-200 bg-white shadow-sm rounded-lg overflow-hidden">
            <thead>
              <tr className="bg-roman-stone text-roman-black border-b border-roman-gold border-b-2">
                {headers.map((h, i) => (
                  <th key={i} className="px-4 py-3 text-left font-display font-bold text-sm uppercase tracking-wider">{parseInline(h)}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {rows.map((row, rI) => (
                <tr key={rI} className="hover:bg-yellow-50/50 transition-colors">
                  {row.map((cell, cI) => (
                    <td key={cI} className="px-4 py-3 font-serif text-gray-800 whitespace-nowrap">{parseInline(cell)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      tableBuffer = [];
    };

    lines.forEach((line, index) => {
      const trimmed = line.trim();
      
      // Table detection logic
      if (trimmed.startsWith('|')) {
        tableBuffer.push(trimmed);
      } else {
        // If we were building a table and hit a non-table line, render the table
        if (tableBuffer.length > 0) flushTable(index);
        
        if (!trimmed) return;

        // Header parsing
        if (trimmed.startsWith('# ')) {
          nodes.push(<h2 key={index} className="text-3xl font-display font-bold text-roman-red mt-8 mb-4 border-b border-gray-200 pb-2">{parseInline(trimmed.substring(2))}</h2>);
        } else if (trimmed.startsWith('## ')) {
          nodes.push(<h3 key={index} className="text-xl font-display font-bold text-roman-black mt-6 mb-3">{parseInline(trimmed.substring(3))}</h3>);
        } else if (trimmed.startsWith('- ')) {
            nodes.push(<li key={index} className="ml-6 list-disc mb-2 text-gray-700 pl-2 font-serif">{parseInline(trimmed.substring(2))}</li>);
        } else {
          nodes.push(<p key={index} className="mb-4 text-gray-700 leading-relaxed font-serif text-lg">{parseInline(trimmed)}</p>);
        }
      }
    });

    // Flush any remaining table at the end
    if (tableBuffer.length > 0) flushTable(lines.length);

    return nodes;
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white min-h-screen">
      <button onClick={onBack} className="flex items-center gap-2 text-gray-500 hover:text-roman-red mb-6 transition-colors">
        <ArrowLeft className="h-4 w-4" /> Volver al Mapa
      </button>

      <article className="mx-auto max-w-none">
        <div className="text-center mb-10">
            <span className="text-roman-gold font-bold uppercase tracking-widest text-sm bg-roman-stone px-3 py-1 rounded-full">Lección {lesson.id}</span>
            <h1 className="font-display text-4xl md:text-5xl text-roman-red mt-4 mb-2">{lesson.title}</h1>
            <p className="font-serif text-xl text-gray-500 italic">{lesson.topic}</p>
        </div>
        
        <div className="bg-roman-paper p-6 rounded-lg mb-10 italic text-gray-700 border-l-4 border-roman-gold shadow-sm">
          {lesson.description}
        </div>

        <div className="space-y-2">
          {renderContent(lesson.content)}
        </div>
      </article>

      <div className="mt-16 pt-8 border-t border-gray-200 flex justify-center pb-12">
        <button
          onClick={handleFinish}
          className="bg-roman-red text-white px-8 py-4 rounded-lg hover:bg-red-900 transition flex items-center gap-3 font-bold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1"
        >
          <CheckCircle className="h-6 w-6" /> Completar Lección & Desbloquear Vocabulario
        </button>
      </div>
    </div>
  );
};

export default LessonView;