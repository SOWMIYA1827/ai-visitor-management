import React, { useEffect, useState } from 'react';
import { packagingService } from '../services/packaging';
import { PackagingMaterial } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import { barrierLabel, barrierColor, capitalize } from '../utils/helpers';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#16a34a', '#1d4ed8', '#dc2626'];

export default function Compare() {
  const [materials, setMaterials] = useState<PackagingMaterial[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    packagingService.list().then(setMaterials).finally(() => setLoading(false));
  }, []);

  const toggle = (id: string) => {
    setSelected(s => s.includes(id) ? s.filter(x => x !== id) : s.length < 3 ? [...s, id] : s);
  };

  const chosen = materials.filter(m => selected.includes(m.id));

  const radarData = ['oxygen_barrier', 'moisture_barrier', 'light_barrier', 'thermal_resistance', 'mechanical_strength'].map(key => ({
    subject: capitalize(key).replace(' barrier', '').replace('Thermal resistance', 'Thermal').replace('Mechanical strength', 'Strength'),
    ...Object.fromEntries(chosen.map(m => [m.name.substring(0, 12), Math.round((m[key as keyof PackagingMaterial] as number) * 100)])),
  }));

  const props: { key: string; label: string }[] = [
    { key: 'oxygen_barrier', label: 'Oxygen Barrier' },
    { key: 'moisture_barrier', label: 'Moisture Barrier' },
    { key: 'light_barrier', label: 'Light Barrier' },
    { key: 'thermal_resistance', label: 'Thermal Resistance' },
    { key: 'mechanical_strength', label: 'Mechanical Strength' },
    { key: 'cost_index', label: 'Cost (lower=cheaper)' },
    { key: 'recyclable', label: 'Recyclable' },
    { key: 'biodegradable', label: 'Biodegradable' },
    { key: 'food_contact_safe', label: 'Food Contact Safe' },
  ];

  const best = (key: string): string => {
    if (!chosen.length) return '';
    const vals = chosen.map(m => {
      const v = m[key as keyof PackagingMaterial];
      return typeof v === 'boolean' ? (v ? 1 : 0) : Number(v);
    });
    const isLowerBetter = key === 'cost_index';
    const bestVal = isLowerBetter ? Math.min(...vals) : Math.max(...vals);
    return chosen[vals.indexOf(bestVal)].id;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Compare Packaging Materials</h1>
        <p className="text-gray-500 text-sm mt-1">Select up to 3 materials to compare side-by-side</p>
      </div>

      {/* Material picker */}
      <Card>
        <CardHeader><CardTitle>Select Materials ({selected.length}/3)</CardTitle></CardHeader>
        <CardBody>
          {loading ? <Spinner /> : (
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
              {materials.map(m => (
                <button key={m.id} onClick={() => toggle(m.id)}
                  disabled={!selected.includes(m.id) && selected.length >= 3}
                  className={`text-left px-3 py-2.5 rounded-lg border-2 text-sm transition ${
                    selected.includes(m.id) ? 'border-green-500 bg-green-50 text-green-800 font-medium'
                    : 'border-gray-200 text-gray-600 hover:border-gray-300 disabled:opacity-40'
                  }`}>
                  {m.name}
                </button>
              ))}
            </div>
          )}
        </CardBody>
      </Card>

      {chosen.length >= 2 && (
        <>
          {/* Radar */}
          <Card>
            <CardHeader><CardTitle>Radar Comparison</CardTitle></CardHeader>
            <CardBody>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11 }} />
                  <PolarRadiusAxis domain={[0, 100]} tick={false} />
                  {chosen.map((m, i) => (
                    <Radar key={m.id} name={m.name} dataKey={m.name.substring(0, 12)}
                      stroke={COLORS[i]} fill={COLORS[i]} fillOpacity={0.15} />
                  ))}
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </CardBody>
          </Card>

          {/* Table */}
          <Card>
            <CardHeader><CardTitle>Detailed Comparison</CardTitle></CardHeader>
            <CardBody className="p-0 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left px-4 py-3 text-xs text-gray-500 uppercase tracking-wider font-medium w-40">Property</th>
                    {chosen.map((m, i) => (
                      <th key={m.id} className="px-4 py-3 text-center text-xs font-semibold" style={{ color: COLORS[i] }}>{m.name}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {props.map(({ key, label }) => {
                    const bestId = best(key);
                    return (
                      <tr key={key} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-gray-600 font-medium text-xs">{label}</td>
                        {chosen.map(m => {
                          const v = m[key as keyof PackagingMaterial];
                          const isNum = typeof v === 'number';
                          const isBool = typeof v === 'boolean';
                          const isB = m.id === bestId;
                          return (
                            <td key={m.id} className={`px-4 py-3 text-center ${isB ? 'bg-green-50' : ''}`}>
                              {isBool ? (
                                <span className={`text-xs font-bold ${v ? 'text-green-600' : 'text-gray-400'}`}>{v ? '✓ Yes' : '✗ No'}</span>
                              ) : isNum && key.includes('barrier') || key.includes('resistance') || key.includes('strength') ? (
                                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${barrierColor(v as number)}`}>{barrierLabel(v as number)}</span>
                              ) : (
                                <span className={`text-xs font-medium ${isB ? 'text-green-700 font-bold' : 'text-gray-700'}`}>{String(v)}</span>
                              )}
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </CardBody>
          </Card>
        </>
      )}
      {chosen.length < 2 && !loading && (
        <div className="text-center py-12 text-gray-400">Select at least 2 materials to compare</div>
      )}
    </div>
  );
}
