import { createContext, useContext, useEffect, useState } from 'react'
import api from '../api/client'

const DEFAULT_THEME = {
  site_name: 'Saurabh Shukla.',
  tagline: 'Build. Automate. Grow.',
  primary_color: '#3B82F6',
  primary_dark_color: '#1D4ED8',
  accent_color: '#22D3EE',
}

const ThemeContext = createContext(DEFAULT_THEME)

/**
 * Fetches the admin-managed theme (GET /settings/theme, public) once on
 * mount and applies it as CSS variables on <html>. Tailwind's electric /
 * electricdim / cyan colors read from these variables (see
 * tailwind.config.js), so every btn-primary, link and accent across the
 * public site updates immediately when an admin changes the Branding
 * settings and the visitor reloads — no rebuild needed.
 */
export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(DEFAULT_THEME)

  useEffect(() => {
    api.get('/settings/theme').then((res) => {
      if (res.data) {
        setTheme((prev) => ({ ...prev, ...res.data }))
        applyThemeVars(res.data)
      }
    }).catch(() => {
      // Keep defaults — the site should never break because the API is down.
    })
  }, [])

  useEffect(() => {
    if (theme.site_name) {
      document.title = theme.site_name
    }
  }, [theme.site_name])

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  )
}

function applyThemeVars(theme) {
  const root = document.documentElement
  if (theme.primary_color) root.style.setProperty('--color-electric', theme.primary_color)
  if (theme.primary_dark_color) root.style.setProperty('--color-electric-dim', theme.primary_dark_color)
  if (theme.accent_color) root.style.setProperty('--color-accent', theme.accent_color)
}

export function useTheme() {
  return useContext(ThemeContext)
}
