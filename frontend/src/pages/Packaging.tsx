import React, { useEffect, useState } from 'react';
import { packagingService } from '../services/packaging';
import { PackagingMaterial } from '../types';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import Badge from '../components/ui/Badge';
import { barrierLabel, barrierColor, capitalize } from '../utils/helpers';
import { Search } from 'lucide-react';

export default function Packaging() {
  const [materials, setMaterials] = useState<PackagingMaterial[]>([]);
  const [filtered, setFiltered] = useState<PackagingMaterial[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    packagingService.list().then(d => { setMaterials(d); setFiltered(d); }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const q = search.toLowerCase();
    setFiltered(materials.filter(m => m.name.toLowerCase().includes(q) || m.material_code.toLowerCase().includes(q) || m.category.includes(q)));
  }, [search, materials]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Packaging Materials Database</h1>
        <p className="text-gray-500 text-sm mt-1">{materials.length} materials in knowledge base</p>
      </div>
      <Card>
        <CardHeader>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search materials…"
              className="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none" />
          </div>
        </CardHeader>
        <CardBody className="p-0">
          {loading ? <div className="flex justify-center py-10"><Spinner /></div> : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
              {filtered.map(m => (
                <div key={m.id} className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-semibold text-gray-900 text-sm">{m.name}</p>
                      <p className="text-xs text-gray-400">{m.material_code} · {capitalize(m.category)}</p>
                    </div>
                    <Badge variant={m.food_contact_safe ? 'green' : 'red'}>{m.food_contact_safe ? 'Food Safe' : 'Not Safe'}</Badge>
                  </div>
                  {m.description && <p className="text-xs text-gray-500 mb-3 line-clamp-2">{m.description}</p>}
                  <div className="grid grid-cols-3 gap-1.5">
                    {[
                      { label: 'O₂', val: m.oxygen_barrier },
                      { label: 'H₂O', val: m.moisture_barrier },
                      { label: 'Light', val: m.light_barrier },
                    ].map(({ label, val }) => (
                      <div key={label} className="text-center">
                        <p className="text-[10px] text-gray-400 mb-0.5">{label}</p>
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${barrierColor(val)}`}>{barrierLabel(val)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex gap-1.5 mt-2 flex-wrap">
                    {m.recyclable && <Badge variant="green">♻️ Recyclable</Badge>}
                    {m.biodegradable && <Badge variant="teal">🌱 Bio</Badge>}
                    {m.compostable && <Badge variant="teal">🍃 Compost</Badge>}
                    {m.bio_based && <Badge variant="teal">🌾 Bio-based</Badge>}
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
