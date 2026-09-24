/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],

  theme: {
    extend: {
      colors: {
        // Core theme colors
        ink: '#0A0E14',
        surface: '#0F1621',
        surface2: '#131C29',
        line: '#1B2432',

        // Light/paper theme
        paper: '#F4F6F9',
        paperline: '#E2E7EE',

        // Text colors
        high: '#EDF1F7',
        muted: '#8C96A6',
        muted2: '#5B6472',

        // Admin Panel tokens
        // Sidebar / Topbar / CrudManager / ModuleShell / etc.
        canvas: '#0B0F17',
        panel: '#0F1621',
        panelline: '#1B2432',
        ink2: '#EDF1F7',

        // CRM lead-status badge colors
        'status-new': '#3B82F6',
        'status-contacted': '#F59E0B',
        'status-qualified': '#A855F7',
        'status-proposal': '#22D3EE',
        'status-negotiation': '#FB923C',
        'status-converted': '#22C55E',
        'status-closed': '#6B7280',

        // Runtime branding colors
        // Values can be changed through CSS variables
        // by ThemeProvider.jsx / Admin Panel branding settings.
        electric: 'var(--color-electric, #3B82F6)',
        electricdim: 'var(--color-electric-dim, #1D4ED8)',
        cyan: 'var(--color-accent, #22D3EE)',
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
};
