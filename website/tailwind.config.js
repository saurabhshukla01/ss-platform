/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0A0E14',
        surface: '#0F1621',
        surface2: '#131C29',
        line: '#1B2432',
        paper: '#F4F6F9',
        paperline: '#E2E7EE',
        high: '#EDF1F7',
        muted: '#8C96A6',
        muted2: '#5B6472',
        electric: '#3B82F6',
        electricdim: '#1D4ED8',
        cyan: '#22D3EE',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
      },
      borderRadius: {
        DEFAULT: '2px',
        sm: '2px',
        md: '3px',
        lg: '4px',
      },
      maxWidth: {
        prose: '68ch',
      },
    },
  },
  plugins: [],
}
