import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronLeft, Zap, AlertCircle } from 'lucide-react';
import { recommendationService } from '../services/recommendations';
import { RecommendFormState, FoodCategory, SensitivityLevel, PerishabilityLevel, TransportationType, PackagingType, Priority, EcoPreference } from '../types';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Button from '../components/ui/Button';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import { FOOD_CATEGORIES, SENSITIVITY_OPTIONS, PERISHABILITY_OPTIONS, TRANSPORTATION_TYPES, PACKAGING_TYPES, PRIORITY_OPTIONS, ECO_PREFERENCES, PACKAGE_SIZES } from '../utils/constants';

const DEMO_DATA: RecommendFormState = {
  food_name: 'Potato Chips', category: 'snacks',
  moisture_content: '2', ph: '5.5', fat_content: '30', protein_content: '6',
  water_activity: '0.3', respiration_rate: '2', perishability: 'low',
  oxygen_sensitivity: 'high', moisture_sensitivity: 'high', light_sensitivity: 'high',
  temperature_sensitivity: 'medium', odor_sensitivity: 'medium', microbial_sensitivity: 'low',
  storage_temp: '25', storage_humidity: '60', storage_duration_days: '180',
  transportation_duration_days: '5', transportation_type: 'road', cold_chain_required: false,
  required_shelf_life_days: '180', package_size: 'medium', package_quantity: '1000',
  budget: '5', packaging_type: 'pouch', priority: 'balanced', eco_preference: 'no_preference',
};

const INITIAL: RecommendFormState = {
  food_name: '', category: 'snacks',
  moisture_content: '', ph: '', fat_content: '', protein_content: '',
  water_activity: '', respiration_rate: '', perishability: 'medium',
  oxygen_sensitivity: 'medium', moisture_sensitivity: 'medium', light_sensitivity: 'medium',
  temperature_sensitivity: 'medium', odor_sensitivity: 'low', microbial_sensitivity: 'medium',
  storage_temp: '25', storage_humidity: '60', storage_duration_days: '30',
  transportation_duration_days: '3', transportation_type: 'road', cold_chain_required: false,
  required_shelf_life_days: '90', package_size: 'medium', package_quantity: '500',
  budget: '5', packaging_type: 'pouch', priority: 'balanced', eco_preference: 'no_preference',
};

const SensitivityPicker = ({ label, value, onChange }: { label: string; value: SensitivityLevel; onChange: (v: SensitivityLevel) => void }) => (
  <div>
    <p className="text-sm font-medium text-gray-700 mb-2">{label}</p>
    <div className="flex gap-2">
      {SENSITIVITY_OPTIONS.map(o => (
        <button key={o.value} type="button" onClick={() => onChange(o.value as SensitivityLevel)}
          className={`flex-1 py-2 text-xs font-medium rounded-lg border-2 transition ${
            value === o.value
              ? o.color === 'green' ? 'border-green-500 bg-green-50 text-green-700'
              : o.color === 'yellow' ? 'border-yellow-500 bg-yellow-50 text-yellow-700'
              : 'border-red-500 bg-red-50 text-red-700'
              : 'border-gray-200 text-gray-500 hover:border-gray-300'
          }`}>
          {o.label}
        </button>
      ))}
    </div>
  </div>
);

const steps = ['Food Information', 'Sensitivities', 'Storage', 'Packaging', 'Sustainability'];

export default function Recommend() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<RecommendFormState>(INITIAL);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k: keyof RecommendFormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(f => ({ ...f, [k]: e.target.value }));
  const setVal = (k: keyof RecommendFormState, v: unknown) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async () => {
    setLoading(true); setError('');
    try {
      const result = await recommendationService.create({
        food_profile: {
          food_name: form.food_name,
          category: form.category as FoodCategory,
          moisture_content: form.moisture_content ? +form.moisture_content : undefined,
          ph: form.ph ? +form.ph : undefined,
          fat_content: form.fat_content ? +form.fat_content : undefined,
          protein_content: form.protein_content ? +form.protein_content : undefined,
          water_activity: form.water_activity ? +form.water_activity : undefined,
          respiration_rate: form.respiration_rate ? +form.respiration_rate : undefined,
          perishability: form.perishability as PerishabilityLevel,
          oxygen_sensitivity: form.oxygen_sensitivity as SensitivityLevel,
          moisture_sensitivity: form.moisture_sensitivity as SensitivityLevel,
          light_sensitivity: form.light_sensitivity as SensitivityLevel,
          temperature_sensitivity: form.temperature_sensitivity as SensitivityLevel,
          odor_sensitivity: form.odor_sensitivity as SensitivityLevel,
          microbial_sensitivity: form.microbial_sensitivity as SensitivityLevel,
        },
        storage_conditions: {
          storage_temp: form.storage_temp ? +form.storage_temp : undefined,
          storage_humidity: form.storage_humidity ? +form.storage_humidity : undefined,
          storage_duration_days: form.storage_duration_days ? +form.storage_duration_days : undefined,
          transportation_duration_days: form.transportation_duration_days ? +form.transportation_duration_days : undefined,
          transportation_type: form.transportation_type as TransportationType,
          cold_chain_required: form.cold_chain_required,
        },
        packaging_requirements: {
          required_shelf_life_days: form.required_shelf_life_days ? +form.required_shelf_life_days : undefined,
          package_size: form.package_size,
          package_quantity: form.package_quantity ? +form.package_quantity : undefined,
          budget: form.budget ? +form.budget : undefined,
          packaging_type: form.packaging_type as PackagingType,
          priority: form.priority as Priority,
          eco_preference: form.eco_preference as EcoPreference,
        },
      });
      navigate(`/results/${result.id}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Failed to generate recommendation. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Create Packaging Recommendation</h1>
        <p className="text-gray-500 text-sm mt-1">Fill in your food details to get an AI-powered packaging recommendation</p>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-2">
        {steps.map((s, i) => (
          <React.Fragment key={s}>
            <div className={`flex items-center gap-2 ${i <= step ? 'text-green-600' : 'text-gray-400'}`}>
              <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold border-2 ${
                i < step ? 'bg-green-600 border-green-600 text-white'
                : i === step ? 'border-green-600 text-green-600'
                : 'border-gray-300 text-gray-400'}`}>{i + 1}</div>
              <span className="hidden sm:block text-xs font-medium">{s}</span>
            </div>
            {i < steps.length - 1 && <div className={`flex-1 h-0.5 ${i < step ? 'bg-green-500' : 'bg-gray-200'}`} />}
          </React.Fragment>
        ))}
      </div>

      {/* Demo button */}
      {step === 0 && (
        <button onClick={() => setForm(DEMO_DATA)} type="button"
          className="w-full border-2 border-dashed border-green-300 text-green-700 py-2.5 rounded-xl text-sm font-medium hover:bg-green-50 transition flex items-center justify-center gap-2">
          <Zap className="w-4 h-4" /> Try Demo — Potato Chips
        </button>
      )}

      <Card>
        <CardHeader><CardTitle>Step {step + 1}: {steps[step]}</CardTitle></CardHeader>
        <CardBody className="space-y-5">
          {/* STEP 1 */}
          {step === 0 && <>
            <Input label="Food Name *" value={form.food_name} onChange={set('food_name')} placeholder="e.g. Potato Chips, Basmati Rice" required />
            <Select label="Food Category *" value={form.category} onChange={set('category')} options={FOOD_CATEGORIES} />
            <div className="grid grid-cols-2 gap-4">
              <Input label="Moisture Content (%)" type="number" min="0" max="100" value={form.moisture_content} onChange={set('moisture_content')} placeholder="0–100" />
              <Input label="pH Value" type="number" min="0" max="14" step="0.1" value={form.ph} onChange={set('ph')} placeholder="0–14" />
              <Input label="Fat Content (%)" type="number" min="0" max="100" value={form.fat_content} onChange={set('fat_content')} placeholder="0–100" />
              <Input label="Protein Content (%)" type="number" min="0" max="100" value={form.protein_content} onChange={set('protein_content')} placeholder="0–100" />
              <Input label="Water Activity (aw)" type="number" min="0" max="1" step="0.01" value={form.water_activity} onChange={set('water_activity')} placeholder="0–1" />
              <Input label="Respiration Rate" type="number" min="0" value={form.respiration_rate} onChange={set('respiration_rate')} placeholder="mg CO₂/kg/h" />
            </div>
            <Select label="Perishability" value={form.perishability} onChange={set('perishability')} options={PERISHABILITY_OPTIONS} />
          </>}

          {/* STEP 2 */}
          {step === 1 && <div className="space-y-4">
            <p className="text-sm text-gray-500 bg-blue-50 border border-blue-100 px-4 py-2 rounded-lg">Rate how sensitive your food is to each factor. Higher sensitivity requires stronger barrier protection.</p>
            <SensitivityPicker label="Oxygen Sensitivity" value={form.oxygen_sensitivity as SensitivityLevel} onChange={v => setVal('oxygen_sensitivity', v)} />
            <SensitivityPicker label="Moisture Sensitivity" value={form.moisture_sensitivity as SensitivityLevel} onChange={v => setVal('moisture_sensitivity', v)} />
            <SensitivityPicker label="Light Sensitivity" value={form.light_sensitivity as SensitivityLevel} onChange={v => setVal('light_sensitivity', v)} />
            <SensitivityPicker label="Temperature Sensitivity" value={form.temperature_sensitivity as SensitivityLevel} onChange={v => setVal('temperature_sensitivity', v)} />
            <SensitivityPicker label="Odor Sensitivity" value={form.odor_sensitivity as SensitivityLevel} onChange={v => setVal('odor_sensitivity', v)} />
            <SensitivityPicker label="Microbial Sensitivity" value={form.microbial_sensitivity as SensitivityLevel} onChange={v => setVal('microbial_sensitivity', v)} />
          </div>}

          {/* STEP 3 */}
          {step === 2 && <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input label="Storage Temperature (°C)" type="number" min="-30" max="60" value={form.storage_temp} onChange={set('storage_temp')} />
              <Input label="Storage Humidity (%)" type="number" min="0" max="100" value={form.storage_humidity} onChange={set('storage_humidity')} />
              <Input label="Storage Duration (days)" type="number" min="1" value={form.storage_duration_days} onChange={set('storage_duration_days')} />
              <Input label="Transport Duration (days)" type="number" min="0" value={form.transportation_duration_days} onChange={set('transportation_duration_days')} />
            </div>
            <Select label="Transportation Type" value={form.transportation_type} onChange={set('transportation_type')} options={TRANSPORTATION_TYPES} />
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Cold Chain Required</p>
              <div className="flex gap-3">
                {[true, false].map(v => (
                  <button key={String(v)} type="button" onClick={() => setVal('cold_chain_required', v)}
                    className={`flex-1 py-2.5 rounded-lg text-sm font-medium border-2 transition ${
                      form.cold_chain_required === v ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-200 text-gray-500 hover:border-gray-300'
                    }`}>
                    {v ? '❄️ Yes' : '✓ No'}
                  </button>
                ))}
              </div>
            </div>
          </div>}

          {/* STEP 4 */}
          {step === 3 && <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input label="Required Shelf Life (days)" type="number" min="1" value={form.required_shelf_life_days} onChange={set('required_shelf_life_days')} />
              <Input label="Package Quantity" type="number" min="1" value={form.package_quantity} onChange={set('package_quantity')} />
            </div>
            <Select label="Package Size" value={form.package_size} onChange={set('package_size')} options={PACKAGE_SIZES} />
            <Input label="Budget per Package (₹)" type="number" min="0" step="0.5" value={form.budget} onChange={set('budget')} placeholder="INR per package" />
            <Select label="Packaging Type" value={form.packaging_type} onChange={set('packaging_type')} options={PACKAGING_TYPES} />
          </div>}

          {/* STEP 5 */}
          {step === 4 && <div className="space-y-5">
            <div>
              <p className="text-sm font-medium text-gray-700 mb-3">Optimization Priority</p>
              <div className="grid grid-cols-1 gap-2">
                {PRIORITY_OPTIONS.map(o => (
                  <button key={o.value} type="button" onClick={() => setVal('priority', o.value)}
                    className={`text-left px-4 py-3 rounded-lg border-2 text-sm font-medium transition ${
                      form.priority === o.value ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'
                    }`}>{o.label}</button>
                ))}
              </div>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-700 mb-3">Eco Preference</p>
              <div className="grid grid-cols-2 gap-2">
                {ECO_PREFERENCES.map(o => (
                  <button key={o.value} type="button" onClick={() => setVal('eco_preference', o.value)}
                    className={`text-left px-3 py-2.5 rounded-lg border-2 text-sm font-medium transition ${
                      form.eco_preference === o.value ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'
                    }`}>{o.label}</button>
                ))}
              </div>
            </div>
          </div>}
        </CardBody>
      </Card>

      {error && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />{error}
        </div>
      )}

      <div className="flex justify-between">
        <Button variant="outline" icon={<ChevronLeft className="w-4 h-4" />} onClick={() => setStep(s => s - 1)} disabled={step === 0}>
          Back
        </Button>
        {step < steps.length - 1 ? (
          <Button icon={<ChevronRight className="w-4 h-4" />} onClick={() => setStep(s => s + 1)}
            disabled={step === 0 && !form.food_name.trim()}>
            Next Step
          </Button>
        ) : (
          <Button size="lg" loading={loading} icon={<Zap className="w-5 h-5" />} onClick={handleSubmit}>
            Generate AI Recommendation
          </Button>
        )}
      </div>
    </div>
  );
}
