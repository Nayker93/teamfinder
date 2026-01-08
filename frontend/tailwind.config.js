/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          cyan: '#00D9FF',
          purple: '#9D00FF',
          green: '#00FF00',
        }
      }
    },
  },
  plugins: [],
}
