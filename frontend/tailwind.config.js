/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          900: "#1e3a8a"
        },
        neon: {
          cyan: '#00D9FF',
          purple: '#9D00FF',
          green: '#00FF00'
        }
      }
    }
  },
  plugins: [],
}
