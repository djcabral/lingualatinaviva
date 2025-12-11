import React, { useState } from 'react';
import { AppView } from './types';
import Dashboard from './components/Dashboard';
import LessonView from './components/LessonView';
import Analyzer from './components/Analyzer';
import SRS from './components/SRS';
import Exercises from './components/Exercises';
import Tutor from './components/Tutor';
import Readings from './components/Readings';
import Challenge from './components/Challenge';
import { Book, Brain, MessageSquare, Search, Menu, X, Globe, LayoutDashboard } from 'lucide-react';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppView>(AppView.DASHBOARD);
  const [viewPayload, setViewPayload] = useState<any>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleViewChange = (view: AppView, payload?: any) => {
    setCurrentView(view);
    if (payload !== undefined) setViewPayload(payload);
    setMobileMenuOpen(false);
  };

  const renderContent = () => {
    switch (currentView) {
      case AppView.ANALYZER: return <Analyzer />;
      case AppView.SRS: return <SRS />;
      case AppView.EXERCISES: return <Exercises />;
      case AppView.TUTOR: return <Tutor />;
      case AppView.LESSON: return <LessonView lessonId={viewPayload} onBack={() => handleViewChange(AppView.DASHBOARD)} onComplete={() => handleViewChange(AppView.DASHBOARD)} />;
      case AppView.READING: return <Readings onBack={() => handleViewChange(AppView.DASHBOARD)} />;
      case AppView.CHALLENGE: return <Challenge lessonId={viewPayload} onBack={() => handleViewChange(AppView.DASHBOARD)} />;
      default: return <Dashboard changeView={handleViewChange} />;
    }
  };

  const NavItem = ({ view, icon: Icon, label }: { view: AppView, icon: any, label: string }) => (
    <button
      onClick={() => handleViewChange(view)}
      className={`flex items-center gap-3 px-4 py-3 w-full text-left rounded-md transition duration-200 ${
        currentView === view 
          ? 'bg-roman-gold text-white font-bold shadow-sm' 
          : 'text-gray-300 hover:bg-white/10 hover:text-white'
      }`}
    >
      <Icon className="h-5 w-5" />
      <span>{label}</span>
    </button>
  );

  return (
    <div className="min-h-screen bg-roman-paper flex font-sans">
      
      {/* Sidebar Desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-roman-black text-white shrink-0 sticky top-0 h-screen">
        <div className="p-6 border-b border-gray-800">
          <div className="flex items-center gap-2 text-roman-gold cursor-pointer" onClick={() => handleViewChange(AppView.DASHBOARD)}>
            <Globe className="h-8 w-8" />
            <h1 className="text-xl font-display font-bold leading-tight">Lingua<br/>Latina Viva</h1>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <NavItem view={AppView.DASHBOARD} icon={LayoutDashboard} label="Mapa" />
          <NavItem view={AppView.ANALYZER} icon={Search} label="Analizador" />
          <NavItem view={AppView.SRS} icon={Brain} label="Vocabulario" />
          <NavItem view={AppView.EXERCISES} icon={Book} label="Ejercicios" />
          <NavItem view={AppView.READING} icon={Book} label="Lecturas" />
          <NavItem view={AppView.TUTOR} icon={MessageSquare} label="Tutor IA" />
        </nav>
        <div className="p-4 text-xs text-gray-500 border-t border-gray-800 text-center">
          &copy; 2024 Lingua Latina Viva
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile Header */}
        <header className="md:hidden bg-roman-black text-white p-4 flex justify-between items-center shadow-md z-20 relative">
          <div className="flex items-center gap-2 text-roman-gold">
            <Globe className="h-6 w-6" />
            <h1 className="text-lg font-display font-bold">Lingua Latina Viva</h1>
          </div>
          <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X /> : <Menu />}
          </button>
        </header>

        {/* Mobile Menu Overlay */}
        {mobileMenuOpen && (
          <div className="md:hidden absolute top-16 left-0 w-full bg-roman-black text-white z-10 shadow-xl border-t border-gray-800">
             <nav className="p-4 space-y-2">
              <NavItem view={AppView.DASHBOARD} icon={LayoutDashboard} label="Mapa" />
              <NavItem view={AppView.ANALYZER} icon={Search} label="Analizador" />
              <NavItem view={AppView.SRS} icon={Brain} label="Vocabulario" />
              <NavItem view={AppView.EXERCISES} icon={Book} label="Ejercicios" />
              <NavItem view={AppView.READING} icon={Book} label="Lecturas" />
              <NavItem view={AppView.TUTOR} icon={MessageSquare} label="Tutor IA" />
            </nav>
          </div>
        )}

        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default App;