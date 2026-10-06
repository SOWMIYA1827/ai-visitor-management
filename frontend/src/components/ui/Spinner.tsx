import React from 'react';
import { Package2 } from 'lucide-react';

export default function Spinner({ size = 'md', className = '' }: { size?: 'sm' | 'md' | 'lg'; className?: string }) {
  const s = { sm: 'w-4 h-4 border-2', md: 'w-8 h-8 border-[3px]', lg: 'w-12 h-12 border-4' }[size];
  return <div className={`${s} border-white/10 border-t-brand-500 rounded-full animate-spin ${className}`} />;
}

export function FullPageSpinner() {
  return (
    <div className="min-h-screen bg-mesh flex items-center justify-center">
      <div className="text-center animate-fade-in">
        <div className="w-20 h-20 glass rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-neon-green">
          <Package2 className="w-10 h-10 text-brand-400 animate-pulse-slow" />
        </div>
        <p className="text-gradient font-bold text-xl mb-1">PackSmart AI</p>
        <p className="text-gray-500 text-sm">Loading…</p>
      </div>
    </div>
  );
}
