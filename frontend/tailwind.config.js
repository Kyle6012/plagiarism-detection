/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-blue': '#0F172A',
        'light-blue': '#1E293B',
        'brand-purple': '#8B5CF6',
        'brand-pink': '#EC4899',
      },
    },
  },
  plugins: [],
}
