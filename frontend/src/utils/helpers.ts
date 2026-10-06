export function scoreColor(score: number): string {
  if (score >= 85) return 'text-brand-400';
  if (score >= 70) return 'text-yellow-400';
  return 'text-red-400';
}

export function scoreBg(score: number): string {
  if (score >= 85) return 'badge-green';
  if (score >= 70) return 'badge-yellow';
  return 'badge-red';
}

export function barrierLabel(value: number): string {
  if (value >= 0.85) return 'Excellent';
  if (value >= 0.65) return 'Good';
  if (value >= 0.40) return 'Fair';
  return 'Poor';
}

export function barrierColor(value: number): string {
  if (value >= 0.85) return 'badge-green';
  if (value >= 0.65) return 'badge-teal';
  if (value >= 0.40) return 'badge-yellow';
  return 'badge-red';
}

export function riskColor(level: string): string {
  if (level === 'High') return 'bg-red-500/10 border-red-500/20 text-red-400';
  if (level === 'Medium') return 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400';
  return 'bg-brand-500/10 border-brand-500/20 text-brand-400';
}

export function daysToReadable(days?: number): string {
  if (!days) return '—';
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''}`;
  if (days < 30) return `${Math.round(days / 7)} week${Math.round(days / 7) !== 1 ? 's' : ''}`;
  if (days < 365) return `${Math.round(days / 30)} month${Math.round(days / 30) !== 1 ? 's' : ''}`;
  return `${(days / 365).toFixed(1)} year${days / 365 >= 2 ? 's' : ''}`;
}

export function shelfLifeRange(min?: number, max?: number): string {
  if (!min && !max) return '—';
  return `${daysToReadable(min)} – ${daysToReadable(max)}`;
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

export function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' ');
}
