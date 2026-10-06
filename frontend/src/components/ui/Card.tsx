import React from 'react';

interface CardProps { children: React.ReactNode; className?: string; hover?: boolean; glow?: boolean; }

export function Card({ children, className = '', hover = false, glow = false }: CardProps) {
  return (
    <div className={`
      glass rounded-2xl
      ${hover ? 'card-3d neon-border cursor-pointer' : ''}
      ${glow ? 'shadow-neon-green' : ''}
      ${className}
    `}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`px-6 py-4 border-b border-white/[0.06] ${className}`}>
      {children}
    </div>
  );
}

export function CardBody({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <div className={`px-6 py-4 ${className}`}>{children}</div>;
}

export function CardTitle({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <h3 className={`text-base font-semibold text-white ${className}`}>{children}</h3>;
}
