/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f0fdf6',
          100: '#d6fbe8',
          200: '#a8f5cc',
          300: '#6aeba9',
          400: '#2ed880',
          500: '#0fbe65',
          600: '#059c52',
          700: '#057a42',
          800: '#075f34',
          900: '#064d2b',
        },
        surface: {
          900: '#060d1a',
          800: '#0a1628',
          700: '#0f2040',
          600: '#152c55',
          500: '#1a3a6e',
        },
        accent: {
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
        },
        neon: {
          green: '#00ff87',
          blue:  '#00cfff',
          purple:'#b57bff',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'hero-mesh':
          'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,255,135,0.18) 0%, transparent 60%), radial-gradient(ellipse 60% 50% at 80% 80%, rgba(0,207,255,0.12) 0%, transparent 60%), linear-gradient(160deg, #060d1a 0%, #0a1628 40%, #0f2040 100%)',
        'card-glass':
          'linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%)',
        'green-glow':
          'radial-gradient(ellipse at center, rgba(0,255,135,0.15) 0%, transparent 70%)',
      },
      boxShadow: {
        'glass':   '0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08)',
        'glass-lg':'0 20px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.10)',
        'neon-green': '0 0 20px rgba(0,255,135,0.4), 0 0 60px rgba(0,255,135,0.15)',
        'neon-blue':  '0 0 20px rgba(0,207,255,0.4), 0 0 60px rgba(0,207,255,0.15)',
        'card-3d':  '0 10px 30px -5px rgba(0,0,0,0.5), 0 4px 12px -2px rgba(0,0,0,0.3)',
        'card-hover':'0 20px 60px -10px rgba(0,0,0,0.6), 0 8px 24px -4px rgba(0,255,135,0.15)',
        'inner-glow':'inset 0 1px 0 rgba(255,255,255,0.12), inset 0 -1px 0 rgba(0,0,0,0.3)',
      },
      animation: {
        'fade-in':    'fadeIn 0.6s ease-out both',
        'slide-up':   'slideUp 0.5s ease-out both',
        'float':      'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        'spin-slow':  'spin 8s linear infinite',
        'shimmer':    'shimmer 2.5s linear infinite',
        'glow-pulse': 'glowPulse 3s ease-in-out infinite',
      },
      keyframes: {
        fadeIn:    { from: { opacity: '0', transform: 'translateY(8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideUp:   { from: { opacity: '0', transform: 'translateY(20px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        float:     { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-12px)' } },
        shimmer:   { from: { backgroundPosition: '-200% 0' }, to: { backgroundPosition: '200% 0' } },
        glowPulse: { '0%,100%': { opacity: '0.6' }, '50%': { opacity: '1' } },
      },
      backdropBlur: { xs: '2px' },
      perspective: { '1000': '1000px', '2000': '2000px' },
    },
  },
  plugins: [],
}
