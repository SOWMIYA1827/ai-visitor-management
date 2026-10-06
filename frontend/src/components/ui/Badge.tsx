import React from 'react';

type BadgeVariant = 'green' | 'blue' | 'yellow' | 'red' | 'gray' | 'teal' | 'purple';

interface BadgeProps { children: React.ReactNode; variant?: BadgeVariant; className?: string; }

export default function Badge({ children, variant = 'gray', className = '' }: BadgeProps) {
  const map: Record<BadgeVariant, string> = {
    green:  'badge-green',
    blue:   'badge-blue',
    yellow: 'badge-yellow',
    red:    'badge-red',
    gray:   'badge-gray',
    teal:   'badge-teal',
    purple: 'bg-purple-500/10 text-purple-300 border border-purple-500/25',
  };
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${map[variant]} ${className}`}>
      {children}
    </span>
  );
}
