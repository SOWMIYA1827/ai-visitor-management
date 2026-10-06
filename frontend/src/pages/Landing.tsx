import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Package2, ShieldCheck, Clock, Brain, Leaf, ChevronRight,
  Droplets, Wind, Thermometer, Sun, Activity, DollarSign, Award, Zap, Star
} from 'lucide-react';
import Navbar from '../components/layout/Navbar';

const steps = [
  { n: 1, title: 'Enter Food Details', desc: 'Food name, category, composition properties.' },
  { n: 2, title: 'Analyze Properties', desc: 'Moisture, pH, fat content, sensitivities.' },
  { n: 3, title: 'AI Evaluates', desc: 'Hybrid rule + ML engine scores 24+ materials.' },
  { n: 4, title: 'Get Recommendation', desc: 'Ranked results with scores & explanations.' },
  { n: 5, title: 'Compare & Report', desc: 'Compare alternatives, download PDF.' },
];

const whyItems = [
  { icon: Droplets, title: 'Moisture Protection', desc: 'Prevent spoilage, mold, and caking.' },
  { icon: Wind, title: 'Oxygen Barrier', desc: 'Block oxidation of fats, vitamins, flavor.' },
  { icon: ShieldCheck, title: 'Microbial Safety', desc: 'Hermetic sealing prevents contamination.' },
  { icon: Sun, title: 'Light Protection', desc: 'Opaque/metallized films block UV damage.' },
  { icon: Thermometer, title: 'Temperature Control', desc: 'Thermal films maintain cold chain integrity.' },
  { icon: Clock, title: 'Extended Shelf Life', desc: 'Right packaging multiplies shelf life 3–10×.' },
  { icon: ShieldCheck, title: 'Food Safety', desc: 'Food-contact certified materials only.' },
  { icon: DollarSign, title: 'Cost Optimization', desc: 'Balance performance with budget constraints.' },
  { icon: Leaf, title: 'Sustainability', desc: 'Explore recyclable & biodegradable options.' },
];

export default function Landing() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-surface-900 text-white overflow-x-hidden">
      <Navbar />

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex items-center bg-mesh overflow-hidden">
        {/* Decorative orbs */}
        <div className="orb w-96 h-96 bg-brand-500/20 top-10 -left-32" style={{ animationDelay: '0s' }} />
        <div className="orb w-80 h-80 bg-accent-500/15 bottom-20 right-10" style={{ animationDelay: '2s' }} />
        <div className="orb w-64 h-64 bg-neon-purple/10 top-40 right-1/3" style={{ animationDelay: '4s' }} />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 py-24 text-center w-full">
          <div className="inline-flex items-center gap-2 glass text-xs px-4 py-2 rounded-full mb-8 border border-brand-500/20 animate-fade-in">
            <Award className="w-3.5 h-3.5 text-brand-400" />
            <span className="text-gray-300">Smart India Hackathon 2026 — Problem ID: 26236 — MoFPI</span>
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black mb-6 leading-[1.05] animate-slide-up">
            Choose the Right<br />
            <span className="text-gradient">Packaging with AI</span>
          </h1>

          <p className="text-lg sm:text-xl text-gray-400 max-w-3xl mx-auto mb-10 leading-relaxed animate-fade-in" style={{ animationDelay: '0.2s' }}>
            PackSmart AI analyzes food characteristics, storage conditions and packaging requirements
            to recommend the most suitable material for better food safety, quality and shelf life.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <Link to="/register"
              className="btn-glow text-white font-bold px-8 py-4 rounded-2xl text-base flex items-center gap-2 justify-center shadow-neon-green">
              <Zap className="w-5 h-5" /> Get Started Free <ChevronRight className="w-4 h-4" />
            </Link>
            <button onClick={() => navigate('/register?demo=1')}
              className="glass text-white font-semibold px-8 py-4 rounded-2xl border border-white/10 hover:border-brand-500/30 hover:bg-white/5 transition text-base">
              🚀 Try Demo — Potato Chips
            </button>
          </div>

          {/* Floating stat cards */}
          <div className="mt-20 grid grid-cols-3 gap-4 max-w-lg mx-auto">
            {[['24+', 'Materials'], ['13', 'Categories'], ['500+', 'Records']].map(([n, l]) => (
              <div key={l} className="glass rounded-2xl p-4 card-3d text-center">
                <div className="text-2xl font-black text-gradient">{n}</div>
                <div className="text-xs text-gray-400 mt-0.5">{l}</div>
              </div>
            ))}
          </div>

          {/* Scroll indicator */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 animate-bounce opacity-50">
            <div className="w-px h-8 bg-gradient-to-b from-transparent to-brand-500" />
            <div className="w-1.5 h-1.5 rounded-full bg-brand-500" />
          </div>
        </div>
      </section>

      {/* ── Feature cards ── */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-surface-900 via-surface-800 to-surface-900" />
        <div className="relative max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-black text-white mb-3">One Platform. Complete Solution.</h2>
            <p className="text-gray-400 max-w-xl mx-auto">AI-powered analysis across all key packaging criteria</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
            {[
              { icon: ShieldCheck, title: 'Food Safety', desc: 'Food-contact certified materials', iconCls: 'bg-brand-500/15 border-brand-500/20', iconColor: 'text-brand-400' },
              { icon: Clock, title: 'Shelf Life', desc: 'Extended shelf-life estimation', iconCls: 'bg-sky-500/15 border-sky-500/20', iconColor: 'text-sky-400' },
              { icon: Brain, title: 'AI Powered', desc: 'Hybrid rule + ML engine', iconCls: 'bg-purple-500/15 border-purple-500/20', iconColor: 'text-purple-400' },
              { icon: Leaf, title: 'Sustainable', desc: 'Eco-friendly alternatives', iconCls: 'bg-teal-500/15 border-teal-500/20', iconColor: 'text-teal-400' },
            ].map(({ icon: Icon, title, desc, iconCls, iconColor }) => (
              <div key={title} className="glass-lg rounded-2xl p-6 card-3d neon-border text-center group">
                <div className={`w-14 h-14 rounded-2xl ${iconCls} border flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className={`w-7 h-7 ${iconColor}`} />
                </div>
                <h3 className="font-bold text-white mb-1">{title}</h3>
                <p className="text-xs text-gray-400">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section id="how-it-works" className="py-24 relative overflow-hidden">
        <div className="orb w-96 h-96 bg-brand-500/10 -right-32 top-0" />
        <div className="relative max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-black text-white mb-3">How It Works</h2>
            <p className="text-gray-400">5 steps to your perfect packaging recommendation</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6 relative">
            {/* Connecting line */}
            <div className="hidden md:block absolute top-8 left-[10%] right-[10%] h-px bg-gradient-to-r from-transparent via-brand-500/30 to-transparent" />
            {steps.map(({ n, title, desc }, i) => (
              <div key={n} className="text-center group animate-slide-up" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="relative inline-block mb-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-brand-600 to-accent-600 rounded-2xl flex items-center justify-center text-2xl font-black text-white shadow-neon-green mx-auto group-hover:scale-110 transition-transform relative z-10">
                    {n}
                  </div>
                  <div className="absolute inset-0 bg-brand-500/20 rounded-2xl blur-xl" />
                </div>
                <h3 className="font-bold text-white text-sm mb-1.5">{title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Why Smart Packaging ── */}
      <section className="py-24 bg-surface-800/50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-black text-white mb-3">Why Smart Packaging Matters</h2>
            <p className="text-gray-400 max-w-xl mx-auto">Wrong packaging = food waste, safety hazards, and revenue loss</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {whyItems.map(({ icon: Icon, title, desc }, i) => (
              <div key={title} className="glass rounded-2xl p-5 flex gap-4 card-3d neon-border group animate-fade-in" style={{ animationDelay: `${i * 0.07}s` }}>
                <div className="w-10 h-10 bg-brand-500/15 border border-brand-500/20 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:bg-brand-500/25 transition-colors">
                  <Icon className="w-5 h-5 text-brand-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-sm mb-0.5">{title}</h3>
                  <p className="text-xs text-gray-500">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-24 relative overflow-hidden">
        <div className="orb w-96 h-96 bg-brand-500/15 -left-32 top-0" />
        <div className="orb w-80 h-80 bg-accent-500/10 right-0 bottom-0" />
        <div className="relative max-w-3xl mx-auto text-center px-4">
          <div className="glass-lg rounded-3xl p-12 border border-brand-500/20">
            <Star className="w-8 h-8 text-brand-400 mx-auto mb-4" />
            <h2 className="text-3xl sm:text-4xl font-black text-white mb-4">
              Ready to Find the<br /><span className="text-gradient">Right Packaging?</span>
            </h2>
            <p className="text-gray-400 mb-8 max-w-lg mx-auto">
              Join farmers, food processors, and manufacturers using AI to make smarter packaging decisions.
            </p>
            <Link to="/register"
              className="btn-glow text-white font-bold px-10 py-4 rounded-2xl text-lg inline-flex items-center gap-2 shadow-neon-green">
              Start Free <ChevronRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="bg-surface-800 border-t border-white/[0.06] py-10 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center justify-center gap-2 mb-3">
            <div className="w-7 h-7 bg-gradient-to-br from-brand-500 to-accent-500 rounded-lg flex items-center justify-center">
              <Package2 className="w-4 h-4 text-white" />
            </div>
            <span className="font-black text-white">PackSmart <span className="text-gradient">AI</span></span>
          </div>
          <p className="text-gray-500 text-sm mb-3">
            AI-Powered Food Packaging Recommendation System<br />
            Smart India Hackathon 2026 · Ministry of Food Processing Industries
          </p>
          <p className="text-xs text-gray-700 max-w-2xl mx-auto">
            PackSmart AI provides preliminary recommendations only. Not a substitute for laboratory testing,
            regulatory compliance, food-contact certification, or expert validation.
          </p>
        </div>
      </footer>
    </div>
  );
}
