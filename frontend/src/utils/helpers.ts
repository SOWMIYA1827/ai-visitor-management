export function scoreColor(score: number): string {
  if (score >= 85) return 'text-green-600';
  if (score >= 70) return 'text-yellow-600';
  return 'text-red-600';
}

export function scoreBg(score: number): string {
  if (score >= 85) return 'bg-green-100 text-green-800';
  if (score >= 70) return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
}

export function barrierLabel(value: number): string {
  if (value >= 0.85) return 'Excellent';
  if (value >= 0.65) return 'Good';
  if (value >= 0.40) return 'Fair';
  return 'Poor';
}

export function barrierColor(value: number): string {
  if (value >= 0.85) return 'bg-green-100 text-green-800';
  if (value >= 0.65) return 'bg-teal-100 text-teal-800';
  if (value >= 0.40) return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
}

export function riskColor(level: string): string {
  if (level === 'High') return 'bg-red-50 border-red-200 text-red-800';
  if (level === 'Medium') return 'bg-yellow-50 border-yellow-200 text-yellow-800';
  return 'bg-green-50 border-green-200 text-green-800';
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
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
}

export function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' ');
}
