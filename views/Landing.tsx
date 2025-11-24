import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, Car } from 'lucide-react';
import { AppView } from '../types';

interface LandingProps {
  onNavigate: (view: AppView) => void;
}

const LandingPage: React.FC<LandingProps> = ({ onNavigate }) => {
  return (
    <div className="h-full flex flex-col items-center justify-center p-6 text-center bg-[url('https://images.unsplash.com/photo-1596451832228-1f9804657315?q=80&w=2500&auto=format&fit=crop')] bg-cover bg-center relative">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/80 z-0"></div>

      <div className="relative z-10 max-w-3xl">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-6xl md:text-8xl font-black text-brand-yellow mb-4 drop-shadow-lg">
            TukTuk Go
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 mb-12 font-light">
            أسرع وأسهل طريقة لحجز توك توك في مدينتك. آمن، سريع، ورخيص.
          </p>
        </motion.div>

        <div className="flex flex-col md:flex-row gap-6 justify-center w-full">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('register-user')}
            className="group flex flex-col items-center justify-center gap-4 bg-brand-yellow text-black w-full md:w-64 h-40 rounded-2xl shadow-xl border-4 border-brand-yellow hover:bg-transparent hover:text-brand-yellow transition-all"
          >
            <MapPin size={48} />
            <span className="text-2xl font-bold">أحتاج توصيلة</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('register-driver')}
            className="group flex flex-col items-center justify-center gap-4 bg-gray-800 text-white w-full md:w-64 h-40 rounded-2xl shadow-xl border-4 border-gray-700 hover:border-brand-yellow transition-all"
          >
            <Car size={48} className="group-hover:text-brand-yellow transition-colors" />
            <span className="text-2xl font-bold group-hover:text-brand-yellow transition-colors">أنا سائق</span>
          </motion.button>
        </div>
      </div>

      {/* Scroll Indicator */}
      <motion.div 
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 2 }}
        className="absolute bottom-8 z-10"
      >
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
          <div className="w-1.5 h-1.5 bg-brand-yellow rounded-full"></div>
        </div>
      </motion.div>
    </div>
  );
};

export default LandingPage;