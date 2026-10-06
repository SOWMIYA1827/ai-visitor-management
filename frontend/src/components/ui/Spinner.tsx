import React from 'react';

export default function Spinner({ size = 'md', className = '' }: { size?: 'sm' | 'md' | 'lg'; className?: string }) {
  const s = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' }[size];
  return <div className={`${s} border-4 border-gray-200 border-t-green-600 rounded-full animate-spin ${className}`} />;
}

export function FullPageSpinner() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <Spinner size="lg" className="mx-auto mb-3" />
        <p className="text-gray-500 text-sm">Loading PackSmart AI…</p>
      </div>
    </div>
  );
}
