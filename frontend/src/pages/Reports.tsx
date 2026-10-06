import React, { useEffect, useState } from 'react';
import { Download } from 'lucide-react';
import { recommendationService } from '../services/recommendations';
import { RecommendationListItem } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import { formatDate, shelfLifeRange, scoreBg } from '../utils/helpers';

export default function Reports() {
  const [recs, setRecs] = useState<RecommendationListItem[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { recommendationService.list().then(setRecs).finally(() => setLoading(false)); }, []);

  return (
    <div className="space-y-6 max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
      <Card>
        <CardHeader><CardTitle>Download PDF Reports</CardTitle></CardHeader>
        <CardBody className="p-0">
          {loading ? <div className="flex justify-center py-10"><Spinner /></div> : recs.length === 0 ? (
            <div className="text-center py-10 text-gray-400">No recommendations yet.</div>
          ) : (
            <div className="divide-y divide-gray-50">
              {recs.map(r => (
                <div key={r.id} className="flex items-center justify-between px-6 py-4 hover:bg-gray-50">
                  <div>
                    <p className="font-medium text-gray-900">{r.food_name || 'Unnamed'}</p>
                    <p className="text-xs text-gray-400">{r.primary_material_name} · {formatDate(r.created_at)}</p>
                    <p className="text-xs text-gray-400">Shelf life: {shelfLifeRange(r.shelf_life_min_days, r.shelf_life_max_days)}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${scoreBg(r.overall_score || 0)}`}>{Math.round(r.overall_score || 0)}%</span>
                    <a href={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/recommendations/${r.id}/report`}
                      target="_blank" rel="noreferrer"
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-green-600 text-white rounded-lg text-xs font-medium hover:bg-green-700 transition">
                      <Download className="w-3.5 h-3.5" /> PDF
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
