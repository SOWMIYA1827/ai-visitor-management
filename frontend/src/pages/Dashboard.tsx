import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { PlusCircle, History, GitCompare, FileText, TrendingUp, Clock, Package } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { recommendationService } from '../services/recommendations';
import { RecommendationListItem } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import { scoreBg, shelfLifeRange, formatDate } from '../utils/helpers';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [recs, setRecs] = useState<RecommendationListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recommendationService.list().then(setRecs).catch(console.error).finally(() => setLoading(false));
  }, []);

  const avgScore = recs.length
    ? Math.round(recs.reduce((s, r) => s + (r.overall_score || 0), 0) / recs.length)
    : 0;

  const chartData = recs.slice(0, 6).reverse().map((r, i) => ({
    name: r.food_name?.substring(0, 8) || `Rec ${i + 1}`,
    score: Math.round(r.overall_score || 0),
  }));

  const stats = [
    { label: 'Total Recommendations', value: recs.length, icon: TrendingUp, color: 'green' },
    { label: 'Avg Score', value: avgScore ? `${avgScore}/100` : '—', icon: Package, color: 'blue' },
    { label: 'Avg Shelf Life', value: recs.length ? `${Math.round(recs.reduce((s,r)=>s+(r.shelf_life_max_days||0),0)/recs.length)} days` : '—', icon: Clock, color: 'purple' },
    { label: 'This Month', value: recs.filter(r => new Date(r.created_at).getMonth() === new Date().getMonth()).length, icon: FileText, color: 'orange' },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div className="bg-gradient-to-r from-blue-900 to-green-700 rounded-2xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-1">Welcome back, {user?.full_name?.split(' ')[0]}! 👋</h1>
        <p className="text-blue-200 text-sm">Ready to find the perfect packaging for your food product?</p>
        <button onClick={() => navigate('/recommend')}
          className="mt-4 bg-green-500 hover:bg-green-400 text-white px-5 py-2.5 rounded-lg font-medium text-sm flex items-center gap-2 w-fit transition">
          <PlusCircle className="w-4 h-4" /> New Recommendation
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <Card key={label}>
            <CardBody className="flex items-center gap-4">
              <div className={`w-10 h-10 bg-${color}-100 rounded-lg flex items-center justify-center flex-shrink-0`}>
                <Icon className={`w-5 h-5 text-${color}-600`} />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{value}</p>
                <p className="text-xs text-gray-500 mt-0.5">{label}</p>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { to: '/recommend', icon: PlusCircle, label: 'New Recommendation', color: 'green' },
          { to: '/history', icon: History, label: 'View History', color: 'blue' },
          { to: '/compare', icon: GitCompare, label: 'Compare Materials', color: 'purple' },
          { to: '/reports', icon: FileText, label: 'Download Reports', color: 'orange' },
        ].map(({ to, icon: Icon, label, color }) => (
          <Link key={to} to={to}
            className={`bg-white border-2 border-${color}-100 hover:border-${color}-300 rounded-xl p-4 flex flex-col items-center gap-2 text-center transition hover:shadow-md`}>
            <div className={`w-10 h-10 bg-${color}-100 rounded-lg flex items-center justify-center`}>
              <Icon className={`w-5 h-5 text-${color}-600`} />
            </div>
            <span className="text-sm font-medium text-gray-700">{label}</span>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Recent recommendations */}
        <Card className="lg:col-span-3">
          <CardHeader className="flex items-center justify-between">
            <CardTitle>Recent Recommendations</CardTitle>
            <Link to="/history" className="text-sm text-green-600 hover:underline">View all</Link>
          </CardHeader>
          <CardBody className="p-0">
            {loading ? (
              <div className="flex justify-center py-10"><Spinner /></div>
            ) : recs.length === 0 ? (
              <div className="text-center py-10 text-gray-400">
                <Package className="w-10 h-10 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No recommendations yet.</p>
                <Link to="/recommend" className="text-green-600 text-sm font-medium mt-1 inline-block hover:underline">Create your first →</Link>
              </div>
            ) : (
              <div className="divide-y divide-gray-50">
                {recs.slice(0, 5).map(r => (
                  <div key={r.id} onClick={() => navigate(`/results/${r.id}`)}
                    className="flex items-center justify-between px-6 py-3.5 hover:bg-gray-50 cursor-pointer transition">
                    <div>
                      <p className="font-medium text-gray-900 text-sm">{r.food_name || 'Unnamed food'}</p>
                      <p className="text-xs text-gray-400">{r.primary_material_name || '—'} • {formatDate(r.created_at)}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-gray-400">{shelfLifeRange(r.shelf_life_min_days, r.shelf_life_max_days)}</span>
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${scoreBg(r.overall_score || 0)}`}>
                        {Math.round(r.overall_score || 0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardBody>
        </Card>

        {/* Chart */}
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle>Score Trend</CardTitle></CardHeader>
          <CardBody>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="score" fill="#16a34a" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-48 flex items-center justify-center text-gray-400 text-sm">No data yet</div>
            )}
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
