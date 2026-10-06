import React, { useEffect, useState } from 'react';
import { adminService } from '../../services/admin';
import { Card, CardBody } from '../../components/ui/Card';
import Spinner from '../../components/ui/Spinner';
import Badge from '../../components/ui/Badge';
import { barrierLabel, barrierColor, capitalize } from '../../utils/helpers';

export default function AdminMaterials() {
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { adminService.getMaterials().then(setMaterials).finally(() => setLoading(false)); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Packaging Materials ({materials.length})</h1>
      <Card>
        <CardBody className="p-0">
          {loading ? <div className="flex justify-center py-10"><Spinner /></div> : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 text-xs text-gray-500 uppercase">
                    <th className="px-4 py-3 text-left">Material</th>
                    <th className="px-4 py-3 text-left">Code</th>
                    <th className="px-4 py-3 text-left">Category</th>
                    <th className="px-4 py-3 text-center">O₂ Barrier</th>
                    <th className="px-4 py-3 text-center">H₂O Barrier</th>
                    <th className="px-4 py-3 text-center">Food Safe</th>
                    <th className="px-4 py-3 text-center">Recyclable</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {materials.map((m: any) => (
                    <tr key={m.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium">{m.name}</td>
                      <td className="px-4 py-3 text-gray-500 font-mono text-xs">{m.material_code}</td>
                      <td className="px-4 py-3"><Badge variant="gray">{capitalize(m.category)}</Badge></td>
                      <td className="px-4 py-3 text-center"><span className={`text-xs font-bold px-2 py-0.5 rounded-full ${barrierColor(m.oxygen_barrier)}`}>{barrierLabel(m.oxygen_barrier)}</span></td>
                      <td className="px-4 py-3 text-center"><span className={`text-xs font-bold px-2 py-0.5 rounded-full ${barrierColor(m.moisture_barrier)}`}>{barrierLabel(m.moisture_barrier)}</span></td>
                      <td className="px-4 py-3 text-center"><Badge variant={m.food_contact_safe ? 'green' : 'red'}>{m.food_contact_safe ? 'Yes' : 'No'}</Badge></td>
                      <td className="px-4 py-3 text-center"><Badge variant={m.recyclable ? 'teal' : 'gray'}>{m.recyclable ? 'Yes' : 'No'}</Badge></td>
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
