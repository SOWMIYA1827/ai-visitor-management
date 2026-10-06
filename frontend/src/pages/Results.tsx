import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Download, GitCompare, ArrowLeft, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { recommendationService } from '../services/recommendations';
import { RecommendationResponse } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import ScoreGauge from '../components/ui/ScoreGauge';
import Spinner from '../components/ui/Spinner';
import { barrierLabel, barrierColor, scoreBg, shelfLifeRange, capitalize } from '../utils/helpers';
import { DISCLAIMER } from '../utils/constants';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

export default function Results() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [rec, setRec] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    recommendationService.getById(id)
      .then(setRec)
      .catch(() => setError('Recommendation not found.'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="flex justify-center py-20"><Spinner size="lg" /></div>;
  if (error || !rec) return <div className="text-center py-20 text-red-500">{error || 'Not found'}</div>;

  const scores = [
    { label: 'Food Safety', value: rec.food_safety_score || 0 },
    { label: 'Barrier', value: (rec.barrier_properties ? Object.values(rec.barrier_properties).reduce((a: number, b) => a + (b as number), 0) / 5 * 100 : 0) },
    { label: 'Shelf Life', value: Math.min(100, ((rec.shelf_life_max_days || 30) / 365) * 100) },
    { label: 'Cost', value: rec.cost_score || 0 },
    { label: 'Sustainability', value: rec.sustainability_score || 0 },
  ];

  const radarData = scores.map(s => ({ subject: s.label, score: Math.round(s.value) }));

  const bp = rec.barrier_properties;

  const riskLevel = (factors: string[]): 'High' | 'Medium' | 'Low' => {
    const lower = factors.join(' ').toLowerCase();
    if (lower.includes('high')) return 'High';
    if (lower.includes('medium')) return 'Medium';
    return 'Low';
  };
  const riskBg = (l: string) =>
    l === 'High' ? 'bg-red-50 border-red-200' : l === 'Medium' ? 'bg-yellow-50 border-yellow-200' : 'bg-green-50 border-green-200';
  const riskIcon = (l: string) =>
    l === 'High' ? <AlertTriangle className="w-4 h-4 text-red-500" /> :
    l === 'Medium' ? <Info className="w-4 h-4 text-yellow-500" /> :
    <CheckCircle className="w-4 h-4 text-green-500" />;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button onClick={() => navigate(-1)} className="text-gray-500 hover:text-gray-700 transition"><ArrowLeft className="w-5 h-5" /></button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Packaging Recommendation</h1>
          <p className="text-gray-500 text-sm">Food: <strong>{rec.food_name || 'Your product'}</strong></p>
        </div>
      </div>

      {/* Best material hero */}
      <Card className="border-2 border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
        <CardBody className="flex flex-col sm:flex-row items-center gap-6 py-6">
          <ScoreGauge score={rec.overall_score || 0} size="lg" label="Overall Score" />
          <div className="flex-1 text-center sm:text-left">
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wide mb-1">Best Packaging</p>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{rec.primary_material?.name || '—'}</h2>
            <p className="text-sm text-gray-600">{rec.packaging_structure}</p>
            <div className="flex flex-wrap gap-2 mt-3 justify-center sm:justify-start">
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${scoreBg(rec.food_safety_score || 0)}`}>Food Safety {Math.round(rec.food_safety_score || 0)}%</span>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${scoreBg(rec.sustainability_score || 0)}`}>Sustainability {Math.round(rec.sustainability_score || 0)}%</span>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${scoreBg(rec.cost_score || 0)}`}>Cost {Math.round(rec.cost_score || 0)}%</span>
            </div>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-400 mb-1">Est. Shelf Life</p>
            <p className="text-lg font-bold text-blue-900">{shelfLifeRange(rec.shelf_life_min_days, rec.shelf_life_max_days)}</p>
            <p className="text-xs text-gray-400 mt-1">Thickness: {rec.recommended_thickness_um?.toFixed(0)} µm</p>
          </div>
        </CardBody>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Explainable AI */}
        <Card>
          <CardHeader><CardTitle>Why This Recommendation?</CardTitle></CardHeader>
          <CardBody>
            <p className="text-sm text-gray-600 leading-relaxed">{rec.explanation}</p>
          </CardBody>
        </Card>

        {/* Radar chart */}
        <Card>
          <CardHeader><CardTitle>Score Breakdown</CardTitle></CardHeader>
          <CardBody>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11 }} />
                <PolarRadiusAxis domain={[0, 100]} tick={false} />
                <Radar dataKey="score" stroke="#16a34a" fill="#16a34a" fillOpacity={0.2} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </CardBody>
        </Card>
      </div>

      {/* Barrier properties */}
      {bp && (
        <Card>
          <CardHeader><CardTitle>Barrier & Physical Properties</CardTitle></CardHeader>
          <CardBody>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              {Object.entries(bp).map(([key, val]) => (
                <div key={key} className="text-center bg-gray-50 rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-1">{capitalize(key).replace(' barrier', '')}</p>
                  <span className={`text-xs font-bold px-2 py-1 rounded-full ${barrierColor(val as number)}`}>
                    {barrierLabel(val as number)}
                  </span>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Alternatives */}
      {rec.alternative_materials && rec.alternative_materials.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Alternative Recommendations</CardTitle></CardHeader>
          <CardBody>
            <div className="space-y-3">
              {rec.alternative_materials.map((mat, i) => (
                <div key={mat.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                  <div className="flex items-center gap-3">
                    <div className="w-7 h-7 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-sm font-bold">{i + 2}</div>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">{mat.name}</p>
                      <p className="text-xs text-gray-400">Category: {capitalize(mat.category)}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right text-xs text-gray-500">
                      <div>O₂: {barrierLabel(mat.oxygen_barrier)}</div>
                      <div>H₂O: {barrierLabel(mat.moisture_barrier)}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Risk factors */}
      {rec.risk_factors && rec.risk_factors.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Risk Factors</CardTitle></CardHeader>
          <CardBody>
            <div className="space-y-2">
              {rec.risk_factors.map((risk, i) => {
                const level = riskLevel([risk]);
                return (
                  <div key={i} className={`flex items-start gap-3 p-3 rounded-lg border ${riskBg(level)}`}>
                    {riskIcon(level)}
                    <p className="text-sm text-gray-700">{risk}</p>
                  </div>
                );
              })}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Storage conditions */}
      {rec.storage_conditions_recommended && (
        <Card>
          <CardHeader><CardTitle>Recommended Storage Conditions</CardTitle></CardHeader>
          <CardBody>
            <p className="text-sm text-gray-600">{rec.storage_conditions_recommended}</p>
          </CardBody>
        </Card>
      )}

      {/* Actions */}
      <div className="flex flex-wrap gap-3">
        <Link to="/compare" className="flex items-center gap-2 px-4 py-2.5 bg-blue-900 text-white rounded-lg text-sm font-medium hover:bg-blue-800 transition">
          <GitCompare className="w-4 h-4" /> Compare Materials
        </Link>
        <a href={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/recommendations/${id}/report`}
          target="_blank" rel="noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 transition">
          <Download className="w-4 h-4" /> Download PDF
        </a>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 flex gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
        <p className="text-xs text-yellow-800 leading-relaxed">{DISCLAIMER}</p>
      </div>
    </div>
  );
}
