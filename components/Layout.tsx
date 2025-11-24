import React from 'react';
import { CarTaxiFront, LogOut } from 'lucide-react';
import { AppView } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  currentView: AppView;
  onNavigate: (view: AppView) => void;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, currentView, onNavigate, onLogout }) => {
  return (
    <div className="min-h-screen flex flex-col bg-brand-black text-white font-sans">
      {/* Header */}
      <header className="bg-brand-yellow text-brand-black py-4 px-6 sticky top-0 z-50 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div 
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => onNavigate('landing')}
          >
            <CarTaxiFront size={32} strokeWidth={2.5} />
            <h1 className="text-2xl font-black tracking-tighter">TukTuk Go</h1>
          </div>
          
          {currentView !== 'landing' && (
            <button 
              onClick={onLogout}
              className="flex items-center gap-2 bg-black/10 hover:bg-black/20 px-3 py-1.5 rounded-full text-sm font-bold transition-colors"
            >
              <LogOut size={16} />
              <span>خروج</span>
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative">
        {children}
      </main>
    </div>
  );
};

export default Layout;