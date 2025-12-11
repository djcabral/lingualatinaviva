import React, { useState, useRef, useEffect } from 'react';
import { getTutorResponse } from '../services/geminiService';
import { ChatMessage } from '../types';
import { Send, User, Bot, Sparkles } from 'lucide-react';

const Tutor: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', text: 'Salve! Soy Marcus, tu Magister. ¿En qué puedo ayudarte hoy con el latín?', timestamp: Date.now() }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: ChatMessage = { role: 'user', text: input, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Filter history for API context
      const history = messages.map(m => ({ role: m.role, text: m.text }));
      const responseText = await getTutorResponse(history, userMsg.text);
      
      const botMsg: ChatMessage = { role: 'model', text: responseText, timestamp: Date.now() };
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      const errorMsg: ChatMessage = { role: 'model', text: 'Mea culpa. Ha ocurrido un error al conectar con el oráculo.', timestamp: Date.now() };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-w-4xl mx-auto bg-white shadow-lg rounded-lg border border-gray-200 overflow-hidden">
      
      {/* Header */}
      <div className="bg-roman-red p-4 flex items-center gap-3 text-white">
        <div className="bg-white/20 p-2 rounded-full">
          <Sparkles className="h-6 w-6" />
        </div>
        <div>
          <h2 className="font-display font-bold text-lg">Magister Marcus</h2>
          <p className="text-xs text-red-100 opacity-90">Tutor de IA experto en latín</p>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-roman-paper">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-end max-w-[80%] gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-gray-700' : 'bg-roman-gold'}`}>
                {msg.role === 'user' ? <User className="h-5 w-5 text-white" /> : <Bot className="h-5 w-5 text-white" />}
              </div>
              <div className={`p-4 rounded-2xl shadow-sm text-sm md:text-base ${
                msg.role === 'user' 
                  ? 'bg-white text-gray-800 rounded-br-none border border-gray-200' 
                  : 'bg-roman-stone text-roman-black rounded-bl-none border border-gray-200 font-serif'
              }`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="flex items-end gap-2">
              <div className="w-8 h-8 rounded-full bg-roman-gold flex items-center justify-center">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <div className="bg-roman-stone p-4 rounded-2xl rounded-bl-none text-gray-500 italic text-sm">
                Marcus cogitat... (pensando)
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex gap-2 relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Pregunta algo en español o latín..."
            className="w-full p-4 pr-12 bg-gray-50 border border-gray-300 rounded-full focus:ring-2 focus:ring-roman-red focus:border-transparent outline-none transition"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="absolute right-2 top-2 p-2 bg-roman-red text-white rounded-full hover:bg-red-900 disabled:opacity-50 transition"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
        <p className="text-center text-xs text-gray-400 mt-2">La IA puede cometer errores. Verifica la información importante.</p>
      </div>
    </div>
  );
};

export default Tutor;
