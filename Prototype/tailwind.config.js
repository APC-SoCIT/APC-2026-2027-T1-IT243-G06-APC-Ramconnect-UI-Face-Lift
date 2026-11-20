/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        apc: {
          gold: '#FDB813',
          goldDark: '#D99805',
          goldLight: '#FEF0CE',
          navy: '#0B1E3D',
          navyLight: '#16284F',
          darkBg: '#09152A',
          cream: '#FFFBF2',
          surface: '#F8F9FA'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
