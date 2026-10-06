import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Package2, ShieldCheck, Clock, Brain, Leaf, ChevronRight,
  Droplets, Wind, Thermometer, Sun, Activity, DollarSign, Award
} from 'lucide-react';
import Navbar from '../components/layout/Navbar';

const steps = [
  { n: 1, title: 'Enter Food Details', desc: 'Provide food name, category, and basic composition properties.' },
  { n: 2, title: 'Analyze Food Properties', desc: 'Specify moisture content, pH, fat content, and sensitivities.' },
  { n: 3, title: 'AI Evaluates Options', desc: 'Our hybrid AI engine filters and scores 24+ packaging materials.' },
  { n: 4, title: 'Get Best Recommendation', desc: 'Receive ranked recommendations with scores and explanations.' },
  { n: 5, title: 'Compare & Download', desc: 'Compare alternatives, download a PDF report, give feedback.' },
];

const features = [
  { icon: Droplets, title: 'Moisture Protection', desc: 'Prevent moisture ingress that causes spoilage, mold, and caking.' },
  { icon: Wind, title: 'Oxygen Barrier', desc: 'Block oxidation that degrades fats, vitamins, and flavor.' },
  { icon: ShieldCheck, title: 'Microbial Protection', desc: 'Prevent contamination with proper hermetic sealing materials.' },
  { icon: Sun, title: 'Light Protection', desc: 'UV and light-sensitive products need opaque or metallized packaging.' },
  { icon: Thermometer, title: 'Temperature Control', desc: 'Thermal-stable films maintain integrity across cold chains.' },
  { icon: Clock, title: 'Extended Shelf Life', desc: 'Right packaging can multiply shelf life by 3–10×.' },
  { icon: ShieldCheck, title: 'Food Safety', desc: 'Food-contact certified materials ensure consumer safety.' },
  { icon: DollarSign, title: 'Cost Optimization', desc: 'Balance barrier performance with packaging budget constraints.' },
  { icon: Leaf, title: 'Sustainability', desc: 'Explore recyclable, biodegradable, and bio-based alternatives.' },
];

export default function Landing() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-white">
      <Navbar />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-green-700 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-64 h-64 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-10 w-96 h-96 bg-green-400 rounded-full blur-3xl" />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 py-24 text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 text-white text-sm px-4 py-1.5 rounded-full mb-6 backdrop-blur-sm border border-white/20">
            <Award className="w-4 h-4" />
            Smart India Hackathon 2026 — Problem ID: 26236
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            Choose the Right<br />
            <span className="text-green-400">Packaging with AI</span>
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-10">
            PackSmart AI analyzes food characteristics, storage conditions and packaging requirements
            to recommend the most suitable packaging material for better food safety, quality and shelf life.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="bg-green-500 hover:bg-green-400 text-white font-semibold px-8 py-4 rounded-xl transition-all shadow-lg flex items-center gap-2 justify-center text-lg">
              Get Started <ChevronRight className="w-5 h-5" />
            </Link>
            <button onClick={() => navigate('/register?demo=1')} className="bg-white/10 hover:bg-white/20 text-white font-semibold px-8 py-4 rounded-xl border border-white/30 transition-all backdrop-blur-sm text-lg">
              Try Demo
            </button>
          </div>

          {/* Stat bar */}
          <div className="mt-16 grid grid-cols-3 gap-6 max-w-2xl mx-auto">
            {[['24+', 'Packaging Materials'], ['13', 'Food Categories'], ['500+', 'Training Records']].map(([n, l]) => (
              <div key={l} className="text-center">
                <div className="text-3xl font-bold text-green-400">{n}</div>
                <div className="text-sm text-blue-200 mt-1">{l}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature cards */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">One Platform, Complete Solution</h2>
            <p className="text-gray-500 max-w-2xl mx-auto">AI-powered analysis across all key packaging selection criteria</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: ShieldCheck, title: 'Food Safety', desc: 'Food-contact certified materials', color: 'green' },
              { icon: Clock, title: 'Shelf Life', desc: 'Extended shelf-life estimation', color: 'blue' },
              { icon: Brain, title: 'AI Powered', desc: 'Hybrid rule + ML engine', color: 'purple' },
              { icon: Leaf, title: 'Sustainable', desc: 'Eco-friendly alternatives', color: 'teal' },
            ].map(({ icon: Icon, title, desc, color }) => (
              <div key={title} className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow text-center">
                <div className={`w-12 h-12 bg-${color}-100 rounded-xl flex items-center justify-center mx-auto mb-4`}>
                  <Icon className={`w-6 h-6 text-${color}-600`} />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
                <p className="text-sm text-gray-500">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">How It Works</h2>
            <p className="text-gray-500">5 simple steps to your AI packaging recommendation</p>
          </div>
          <div className="relative">
            <div className="hidden md:block absolute top-8 left-1/2 -translate-x-1/2 w-3/4 h-0.5 bg-green-100" />
            <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
              {steps.map(({ n, title, desc }) => (
                <div key={n} className="relative text-center">
                  <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 shadow-lg relative z-10">
                    {n}
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
                  <p className="text-sm text-gray-500">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Why Smart Packaging */}
      <section className="py-20 bg-gradient-to-br from-green-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Why Smart Packaging Matters</h2>
            <p className="text-gray-500">Wrong packaging leads to food waste, safety issues, and revenue loss</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-white rounded-xl p-6 shadow-sm flex gap-4 hover:shadow-md transition-shadow">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Icon className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
                  <p className="text-sm text-gray-500">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-blue-900 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Find the Right Packaging?</h2>
        <p className="text-blue-200 mb-8 max-w-xl mx-auto">Join farmers, food processors, and manufacturers using AI to make smarter packaging decisions.</p>
        <Link to="/register" className="bg-green-500 hover:bg-green-400 text-white font-semibold px-8 py-4 rounded-xl transition-all inline-flex items-center gap-2 text-lg">
          Start Free <ChevronRight className="w-5 h-5" />
        </Link>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-10 text-center text-sm">
        <div className="max-w-4xl mx-auto px-4">
          <p className="text-white font-semibold mb-2">PackSmart AI</p>
          <p className="mb-4">AI-Powered Food Packaging Recommendation System | Smart India Hackathon 2026 | Ministry of Food Processing Industries</p>
          <p className="text-xs text-gray-600">
            PackSmart AI provides preliminary recommendations only. Not a substitute for laboratory testing, regulatory compliance, or expert validation.
          </p>
        </div>
      </footer>
    </div>
  );
}
