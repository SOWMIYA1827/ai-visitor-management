import React from 'react';

interface ScoreGaugeProps { score: number; size?: 'sm' | 'md' | 'lg'; label?: string; }

export default function ScoreGauge({ score, size = 'md', label }: ScoreGaugeProps) {
  const r     = { sm: 28, md: 44, lg: 60 }[size];
  const stroke= { sm: 5,  md: 7,  lg: 9  }[size];
  const fs    = { sm: 'text-lg', md: 'text-3xl', lg: 'text-5xl' }[size];
  const dim   = (r + stroke) * 2;
  const circ  = 2 * Math.PI * r;
  const offset= circ - (score / 100) * circ;
  const color = score >= 85 ? '#00ff87' : score >= 70 ? '#fbbf24' : '#f87171';
  const glow  = score >= 85 ? '0 0 20px rgba(0,255,135,0.5)' : score >= 70 ? '0 0 20px rgba(251,191,36,0.5)' : '0 0 20px rgba(248,113,113,0.5)';

  return (
    <div className="flex flex-col items-center gap-1.5">
      <div className="relative" style={{ width: dim, height: dim }}>
        <svg width={dim} height={dim} className="-rotate-90">
          <circle cx={r+stroke} cy={r+stroke} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={stroke} />
          <circle cx={r+stroke} cy={r+stroke} r={r} fill="none" stroke={color} strokeWidth={stroke}
            strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)', filter: `drop-shadow(${glow})` }} />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`${fs} font-black`} style={{ color }}>{Math.round(score)}</span>
        </div>
      </div>
      {label && <span className="text-xs text-gray-400 text-center font-medium">{label}</span>}
    </div>
  );
}
