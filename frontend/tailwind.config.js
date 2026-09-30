/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#090d16',
        surface: '#111827',
        'surface-elevated': '#1f2937',
        border: '#1f293d',
        accent: '#06b6d4',
        'accent-hazard': '#ef4444',
        'accent-warning': '#f59e0b',
        'accent-safe': '#10b981',
      },
    },
  },
  plugins: [],
}
