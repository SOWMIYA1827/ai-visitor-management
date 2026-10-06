import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { PlusCircle, History, GitCompare, FileText, TrendingUp, Clock, Package, Zap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { recommendationService } from '../services/recommendations';
import { RecommendationListItem } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import { scoreBg, shelfLifeRange, formatDate } from '../utils/helpers';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload?.length) {
    return (
      <div className="glass rounded-xl px-3 py-2 text-xs border border-brand-500/20">
        <p className="text-gray-400">{label}</p>
        <p className="text-brand-400 font-bold">{payload[0].value}%</p>
      </div>
    );
  }
  return null;
};

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [recs, setRecs] = useState<RecommendationListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recommendationService.list().then(setRecs).catch(console.error).finally(() => setLoading(false));
  }, []);

  const avgScore = recs.length ? Math.round(recs.reduce((s, r) => s + (r.overall_score || 0), 0) / recs.length) : 0;
  const chartData = recs.slice(0, 6).reverse().map((r, i) => ({
    name: r.food_name?.substring(0, 8) || `R${i + 1}`,
    score: Math.round(r.overall_score || 0),
  }));

  const stats = [
    { label: 'Total', value: recs.length, icon: TrendingUp, iconCls: 'bg-brand-500/15 border-brand-500/20', iconColor: 'text-brand-400' },
    { label: 'Avg Score', value: avgScore ? `${avgScore}%` : '—', icon: Package, iconCls: 'bg-sky-500/15 border-sky-500/20', iconColor: 'text-sky-400' },
    { label: 'Avg Shelf Life', value: recs.length ? `${Math.round(recs.reduce((s, r) => s + (r.shelf_life_max_days || 0), 0) / recs.length)}d` : '—', icon: Clock, iconCls: 'bg-purple-500/15 border-purple-500/20', iconColor: 'text-purple-400' },
    { label: 'This Month', value: recs.filter(r => new Date(r.created_at).getMonth() === new Date().getMonth()).length, icon: FileText, iconCls: 'bg-yellow-500/15 border-yellow-500/20', iconColor: 'text-yellow-400' },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome hero */}
      <div className="relative overflow-hidden glass rounded-2xl p-6 border border-brand-500/20">
        <div className="orb w-64 h-64 bg-brand-500/20 -right-10 -top-10" />
        <div className="orb w-48 h-48 bg-accent-500/10 right-20 bottom-0" />
        <div className="relative">
          <h1 className="text-2xl font-black text-white mb-1">
            Welcome back, <span className="text-gradient">{user?.full_name?.split(' ')[0]}</span>! 👋
          </h1>
          <p className="text-gray-400 text-sm mb-4">Ready to find the perfect packaging for your food product?</p>
          <button onClick={() => navigate('/recommend')}
            className="btn-glow text-white px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center gap-2 w-fit">
            <PlusCircle className="w-4 h-4" /> New Recommendation
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, iconCls, iconColor }) => (
          <Card key={label} className="card-3d">
            <CardBody className="flex items-center gap-4">
              <div className={`w-11 h-11 ${iconCls} border rounded-xl flex items-center justify-center flex-shrink-0`}>
                <Icon className={`w-5 h-5 ${iconColor}`} />
              </div>
              <div>
                <p className="text-xl font-black text-white">{value}</p>
                <p className="text-xs text-gray-500 mt-0.5">{label}</p>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { to: '/recommend', icon: PlusCircle, label: 'New Recommendation', iconCls: 'bg-brand-500/15 border-brand-500/20', iconColor: 'text-brand-400' },
          { to: '/history', icon: History, label: 'View History', iconCls: 'bg-sky-500/15 border-sky-500/20', iconColor: 'text-sky-400' },
          { to: '/compare', icon: GitCompare, label: 'Compare Materials', iconCls: 'bg-purple-500/15 border-purple-500/20', iconColor: 'text-purple-400' },
          { to: '/reports', icon: FileText, label: 'Download Reports', iconCls: 'bg-yellow-500/15 border-yellow-500/20', iconColor: 'text-yellow-400' },
        ].map(({ to, icon: Icon, label, iconCls, iconColor }) => (
          <Link key={to} to={to} className="glass neon-border rounded-2xl p-4 flex flex-col items-center gap-2.5 text-center transition hover:bg-white/[0.04] card-3d group">
            <div className={`w-11 h-11 ${iconCls} border rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform`}>
              <Icon className={`w-5 h-5 ${iconColor}`} />
            </div>
            <span className="text-xs font-semibold text-gray-300">{label}</span>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
        {/* Recent */}
        <Card className="lg:col-span-3">
          <CardHeader className="flex items-center justify-between">
            <CardTitle>Recent Recommendations</CardTitle>
            <Link to="/history" className="text-xs text-brand-400 hover:text-brand-300 font-medium transition">View all →</Link>
          </CardHeader>
          <CardBody className="p-0">
            {loading ? (
              <div className="flex justify-center py-10"><Spinner /></div>
            ) : recs.length === 0 ? (
              <div className="text-center py-12 text-gray-600">
                <Package className="w-10 h-10 mx-auto mb-2 opacity-20" />
                <p className="text-sm">No recommendations yet.</p>
                <Link to="/recommend" className="text-brand-400 text-sm font-medium mt-1 inline-block hover:text-brand-300">
                  Create your first →
                </Link>
              </div>
            ) : (
              <div>
                {recs.slice(0, 5).map(r => (
                  <div key={r.id} onClick={() => navigate(`/results/${r.id}`)}
                    className="flex items-center justify-between px-6 py-3.5 hover:bg-white/[0.03] cursor-pointer transition border-b border-white/[0.04] last:border-0">
                    <div>
                      <p className="font-semibold text-gray-200 text-sm">{r.food_name || 'Unnamed food'}</p>
                      <p className="text-xs text-gray-600">{r.primary_material_name || '—'} · {formatDate(r.created_at)}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-gray-600">{shelfLifeRange(r.shelf_life_min_days, r.shelf_life_max_days)}</span>
                      <span className={`score-pill ${scoreBg(r.overall_score || 0)}`}>{Math.round(r.overall_score || 0)}%</span>
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
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                  <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#6b7280' }} axisLine={false} tickLine={false} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#6b7280' }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="score" fill="url(#barGrad)" radius={[6, 6, 0, 0]} />
                  <defs>
                    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#0fbe65" />
                      <stop offset="100%" stopColor="#057a42" />
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-48 flex items-center justify-center text-gray-600 text-sm">No data yet</div>
            )}
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
