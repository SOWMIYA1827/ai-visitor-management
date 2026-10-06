import React from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string; error?: string; options: { value: string; label: string }[];
}

export default function Select({ label, error, options, className = '', id, ...props }: SelectProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1.5">
          {label}
        </label>
      )}
      <select
        id={inputId}
        className={`input-dark appearance-none cursor-pointer ${error ? '!border-red-500/60' : ''} ${className}`}
        style={{ background: '#0a1628' }}
        {...props}
      >
        {options.map(o => <option key={o.value} value={o.value} style={{ background: '#0a1628' }}>{o.label}</option>)}
      </select>
      {error && <p className="mt-1.5 text-xs text-red-400">{error}</p>}
    </div>
  );
}
