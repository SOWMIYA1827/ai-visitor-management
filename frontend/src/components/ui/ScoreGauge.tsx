import React from 'react';

interface ScoreGaugeProps { score: number; size?: 'sm' | 'md' | 'lg'; label?: string; }

export default function ScoreGauge({ score, size = 'md', label }: ScoreGaugeProps) {
  const r = { sm: 28, md: 42, lg: 56 }[size];
  const stroke = { sm: 5, md: 7, lg: 9 }[size];
  const fontSize = { sm: 'text-lg', md: 'text-3xl', lg: 'text-4xl' }[size];
  const dim = (r + stroke) * 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 85 ? '#16a34a' : score >= 70 ? '#ca8a04' : '#dc2626';

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative" style={{ width: dim, height: dim }}>
        <svg width={dim} height={dim} className="-rotate-90">
          <circle cx={r + stroke} cy={r + stroke} r={r} fill="none" stroke="#e5e7eb" strokeWidth={stroke} />
          <circle cx={r + stroke} cy={r + stroke} r={r} fill="none" stroke={color} strokeWidth={stroke}
            strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1s ease' }} />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`${fontSize} font-bold`} style={{ color }}>{Math.round(score)}</span>
        </div>
      </div>
      {label && <span className="text-xs text-gray-500 text-center">{label}</span>}
    </div>
  );
}
