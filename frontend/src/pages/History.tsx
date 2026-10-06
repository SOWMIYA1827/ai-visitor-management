import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Download, Eye, Package } from 'lucide-react';
import { recommendationService } from '../services/recommendations';
import { RecommendationListItem } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import { scoreBg, shelfLifeRange, formatDate } from '../utils/helpers';

export default function History() {
  const navigate = useNavigate();
  const [recs, setRecs] = useState<RecommendationListItem[]>([]);
  const [filtered, setFiltered] = useState<RecommendationListItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recommendationService.list().then(data => { setRecs(data); setFiltered(data); }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const q = search.toLowerCase();
    setFiltered(recs.filter(r =>
      r.food_name?.toLowerCase().includes(q) || r.primary_material_name?.toLowerCase().includes(q)
    ));
  }, [search, recs]);

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Recommendation History</h1>
          <p className="text-gray-500 text-sm mt-1">{recs.length} total recommendations</p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Search by food name or material…"
                className="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none" />
            </div>
          </div>
        </CardHeader>
        <CardBody className="p-0">
          {loading ? (
            <div className="flex justify-center py-12"><Spinner /></div>
          ) : filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              <Package className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p>No recommendations found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wider">
                    <th className="px-6 py-3 font-medium">Food</th>
                    <th className="px-6 py-3 font-medium">Recommended Material</th>
                    <th className="px-6 py-3 font-medium">Shelf Life</th>
                    <th className="px-6 py-3 font-medium">Score</th>
                    <th className="px-6 py-3 font-medium">Date</th>
                    <th className="px-6 py-3 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {filtered.map(r => (
                    <tr key={r.id} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4 font-medium text-gray-900">{r.food_name || '—'}</td>
                      <td className="px-6 py-4 text-gray-600">{r.primary_material_name || '—'}</td>
                      <td className="px-6 py-4 text-gray-600">{shelfLifeRange(r.shelf_life_min_days, r.shelf_life_max_days)}</td>
                      <td className="px-6 py-4">
                        <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${scoreBg(r.overall_score || 0)}`}>
                          {Math.round(r.overall_score || 0)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-500">{formatDate(r.created_at)}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button onClick={() => navigate(`/results/${r.id}`)}
                            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition" title="View">
                            <Eye className="w-4 h-4" />
                          </button>
                          <a href={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/recommendations/${r.id}/report`}
                            target="_blank" rel="noreferrer"
                            className="p-1.5 text-green-600 hover:bg-green-50 rounded-lg transition" title="Download PDF">
                            <Download className="w-4 h-4" />
                          </a>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
