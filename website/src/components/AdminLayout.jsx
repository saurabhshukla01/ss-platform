import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const NAVIGATION = [
  {
    section: 'Overview',
    items: [
      {
        label: 'Dashboard',
        path: '/admin',
        icon: '▦',
      },
      {
        label: 'Analytics',
        path: '/admin/analytics',
        icon: '◔',
      },
    ],
  },

  {
    section: 'CRM',
    items: [
      {
        label: 'Leads',
        path: '/admin/crm',
        icon: '◎',
      },
      {
        label: 'Inquiries',
        path: '/admin/crm/inquiries',
        icon: '▤',
      },
    ],
  },

  {
    section: 'Business',
    items: [
      {
        label: 'Services',
        path: '/admin/services',
        icon: '◆',
      },
      {
        label: 'Subscriptions',
        path: '/admin/subscriptions',
        icon: '↻',
      },
      {
        label: 'Payments',
        path: '/admin/payments',
        icon: '₹',
      },
    ],
  },

  {
    section: 'Website',
    items: [
      {
        label: 'Website',
        path: '/admin/website',
        icon: '⌂',
      },
      {
        label: 'Content',
        path: '/admin/content',
        icon: '▣',
      },
      {
        label: 'SEO',
        path: '/admin/seo',
        icon: '⌕',
      },
    ],
  },

  {
    section: 'System',
    items: [
      {
        label: 'Communication',
        path: '/admin/communication',
        icon: '◉',
      },
      {
        label: 'Settings',
        path: '/admin/settings',
        icon: '⚙',
      },
      {
        label: 'Audit Logs',
        path: '/admin/audit-logs',
        icon: '≡',
      },
    ],
  },
]

export default function AdminLayout({
  title,
  children,
}) {
  const { admin, logout } = useAuth()

  const location = useLocation()

  const [mobileOpen, setMobileOpen] =
    useState(false)

  const [profileOpen, setProfileOpen] =
    useState(false)

  /*
  |--------------------------------------------------------------------------
  | Initials
  |--------------------------------------------------------------------------
  */

  const displayName =
    admin?.full_name ||
    admin?.name ||
    'Administrator'

  const email =
    admin?.email ||
    'admin@example.com'

  const initials =
    displayName
      .split(' ')
      .filter(Boolean)
      .map((word) => word[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'AD'

  /*
  |--------------------------------------------------------------------------
  | Active Route
  |--------------------------------------------------------------------------
  */

  function isActive(path) {
    if (path === '/admin') {
      return (
        location.pathname ===
        '/admin'
      )
    }

    return (
      location.pathname === path ||
      location.pathname.startsWith(
        `${path}/`,
      )
    )
  }

  /*
  |--------------------------------------------------------------------------
  | Close Mobile Sidebar
  |--------------------------------------------------------------------------
  */

  function closeMobileSidebar() {
    setMobileOpen(false)
  }

  return (
    <div
      className="
        fixed
        inset-0
        overflow-hidden
        bg-app
        text-ink2
      "
    >
      {/* ============================================================
          MOBILE OVERLAY
          ============================================================ */}

      {mobileOpen && (
        <button
          type="button"
          aria-label="Close navigation"
          onClick={
            closeMobileSidebar
          }
          className="
            fixed
            inset-0
            z-40
            bg-black/60
            backdrop-blur-sm
            lg:hidden
          "
        />
      )}

      {/* ============================================================
          SIDEBAR
          ============================================================ */}

      <aside
        className={`
          fixed
          inset-y-0
          left-0
          z-50
          flex
          w-[260px]
          flex-col
          border-r
          border-panelline
          bg-sidebar
          shadow-2xl
          transition-transform
          duration-300
          lg:translate-x-0
          ${
            mobileOpen
              ? 'translate-x-0'
              : '-translate-x-full'
          }
        `}
      >
        {/* ========================================================
            LOGO
            ======================================================== */}

        <div
          className="
            flex
            h-[72px]
            shrink-0
            items-center
            border-b
            border-panelline
            px-5
          "
        >
          <Link
            to="/admin"
            onClick={
              closeMobileSidebar
            }
            className="
              flex
              items-center
              gap-3
              no-underline
            "
          >
            <div
              className="
                flex
                h-10
                w-10
                items-center
                justify-center
                rounded-xl
                bg-gradient-to-br
                from-cyan-400
                to-blue-600
                text-sm
                font-black
                text-white
                shadow-lg
                shadow-cyan-500/20
              "
            >
              SS
            </div>

            <div>
              <div
                className="
                  text-base
                  font-bold
                  tracking-tight
                  text-ink2
                "
              >
                SS Platform
                <span className="text-cyan-400">
                  .
                </span>
              </div>

              <div
                className="
                  mt-0.5
                  text-[9px]
                  font-semibold
                  uppercase
                  tracking-[0.18em]
                  text-muted
                "
              >
                Administration
              </div>
            </div>
          </Link>

          {/* Mobile close */}

          <button
            type="button"
            onClick={
              closeMobileSidebar
            }
            className="
              ml-auto
              rounded-lg
              p-2
              text-muted
              hover:bg-white/5
              hover:text-ink2
              lg:hidden
            "
          >
            ×
          </button>
        </div>

        {/* ========================================================
            NAVIGATION
            ======================================================== */}

        <nav
          className="
            min-h-0
            flex-1
            overflow-y-auto
            overflow-x-hidden
            px-3
            py-4
          "
        >
          <div className="space-y-5">
            {NAVIGATION.map(
              (section) => (
                <div
                  key={
                    section.section
                  }
                >
                  <div
                    className="
                      mb-2
                      px-3
                      text-[9px]
                      font-bold
                      uppercase
                      tracking-[0.18em]
                      text-muted
                    "
                  >
                    {
                      section.section
                    }
                  </div>

                  <div className="space-y-1">
                    {section.items.map(
                      (item) => {
                        const active =
                          isActive(
                            item.path,
                          )

                        return (
                          <Link
                            key={
                              item.path
                            }
                            to={
                              item.path
                            }
                            onClick={
                              closeMobileSidebar
                            }
                            className={`
                              group
                              relative
                              flex
                              items-center
                              gap-3
                              rounded-xl
                              px-3
                              py-2.5
                              text-sm
                              font-medium
                              no-underline
                              transition
                              duration-150
                              ${
                                active
                                  ? `
                                    bg-cyan-400/10
                                    text-cyan-400
                                  `
                                  : `
                                    text-muted
                                    hover:bg-white/[0.04]
                                    hover:text-ink2
                                  `
                              }
                            `}
                          >
                            {active && (
                              <span
                                className="
                                  absolute
                                  -left-3
                                  top-1/2
                                  h-6
                                  w-0.5
                                  -translate-y-1/2
                                  rounded-r-full
                                  bg-cyan-400
                                "
                              />
                            )}

                            <span
                              className={`
                                flex
                                h-8
                                w-8
                                shrink-0
                                items-center
                                justify-center
                                rounded-lg
                                text-sm
                                ${
                                  active
                                    ? 'bg-cyan-400/10'
                                    : 'bg-white/[0.03]'
                                }
                              `}
                            >
                              {
                                item.icon
                              }
                            </span>

                            <span className="truncate">
                              {
                                item.label
                              }
                            </span>

                            {active && (
                              <span
                                className="
                                  ml-auto
                                  h-1.5
                                  w-1.5
                                  rounded-full
                                  bg-cyan-400
                                "
                              />
                            )}
                          </Link>
                        )
                      },
                    )}
                  </div>
                </div>
              ),
            )}
          </div>
        </nav>

        {/* ========================================================
            SIDEBAR FOOTER
            ======================================================== */}

        <div
          className="
            shrink-0
            border-t
            border-panelline
            p-3
          "
        >
          <div
            className="
              flex
              items-center
              gap-3
              rounded-xl
              bg-white/[0.025]
              p-3
            "
          >
            <div
              className="
                flex
                h-9
                w-9
                shrink-0
                items-center
                justify-center
                rounded-lg
                bg-gradient-to-br
                from-slate-600
                to-slate-800
                text-[11px]
                font-bold
                text-white
              "
            >
              {initials}
            </div>

            <div className="min-w-0">
              <p
                className="
                  truncate
                  text-xs
                  font-semibold
                  text-ink2
                "
              >
                {displayName}
              </p>

              <p
                className="
                  mt-0.5
                  truncate
                  text-[10px]
                  text-muted
                "
              >
                {email}
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* ============================================================
          MAIN AREA
          ============================================================ */}

      <div
        className="
          flex
          h-full
          min-w-0
          flex-col
          lg:pl-[260px]
        "
      >
        {/* ==========================================================
            FIXED HEADER
            ========================================================== */}

        <header
          className="
            relative
            z-30
            flex
            h-[72px]
            shrink-0
            items-center
            border-b
            border-panelline
            bg-panel
            px-4
            shadow-sm
            sm:px-6
          "
        >
          <div className="flex min-w-0 flex-1 items-center gap-3">
            {/* Mobile menu */}

            <button
              type="button"
              onClick={() =>
                setMobileOpen(
                  true,
                )
              }
              className="
                flex
                h-10
                w-10
                shrink-0
                items-center
                justify-center
                rounded-xl
                border
                border-panelline
                bg-white/[0.02]
                text-muted
                hover:text-ink2
                lg:hidden
              "
              aria-label="Open navigation"
            >
              ☰
            </button>

            {/* Page title */}

            <div className="min-w-0">
              <h1
                className="
                  truncate
                  text-lg
                  font-bold
                  tracking-tight
                  text-ink2
                  sm:text-xl
                "
              >
                {title ||
                  'Dashboard'}
              </h1>

              <div
                className="
                  hidden
                  items-center
                  gap-2
                  text-[10px]
                  text-muted
                  sm:flex
                "
              >
                <span>
                  SS Platform
                </span>

                <span>•</span>

                <span>
                  Administration
                </span>
              </div>
            </div>
          </div>

          {/* ========================================================
              HEADER ACTIONS
              ======================================================== */}

          <div className="flex shrink-0 items-center gap-2">
            {/* Status */}

            <div
              className="
                hidden
                items-center
                gap-2
                rounded-full
                border
                border-emerald-500/20
                bg-emerald-500/[0.06]
                px-3
                py-1.5
                text-[10px]
                font-medium
                text-emerald-400
                sm:flex
              "
            >
              <span
                className="
                  h-1.5
                  w-1.5
                  rounded-full
                  bg-emerald-400
                "
              />

              System Online
            </div>

            {/* Notification */}

            <button
              type="button"
              className="
                relative
                flex
                h-10
                w-10
                items-center
                justify-center
                rounded-xl
                border
                border-panelline
                bg-white/[0.02]
                text-muted
                transition
                hover:bg-white/[0.05]
                hover:text-ink2
              "
              title="Notifications"
            >
              ♢

              <span
                className="
                  absolute
                  right-2.5
                  top-2
                  h-1.5
                  w-1.5
                  rounded-full
                  bg-cyan-400
                "
              />
            </button>

            {/* Profile */}

            <div className="relative">
              <button
                type="button"
                onClick={() =>
                  setProfileOpen(
                    (value) =>
                      !value,
                  )
                }
                className="
                  flex
                  items-center
                  gap-2
                  rounded-xl
                  border
                  border-panelline
                  bg-white/[0.02]
                  p-1.5
                  pr-2.5
                  transition
                  hover:bg-white/[0.05]
                "
              >
                <div
                  className="
                    flex
                    h-8
                    w-8
                    items-center
                    justify-center
                    rounded-lg
                    bg-gradient-to-br
                    from-cyan-400
                    to-blue-600
                    text-[10px]
                    font-bold
                    text-white
                  "
                >
                  {initials}
                </div>

                <span
                  className="
                    hidden
                    max-w-[110px]
                    truncate
                    text-xs
                    font-semibold
                    text-ink2
                    md:block
                  "
                >
                  {displayName}
                </span>

                <span className="text-[10px] text-muted">
                  ▾
                </span>
              </button>

              {/* Profile dropdown */}

              {profileOpen && (
                <div
                  className="
                    absolute
                    right-0
                    top-12
                    z-50
                    w-60
                    overflow-hidden
                    rounded-xl
                    border
                    border-panelline
                    bg-panel
                    shadow-2xl
                  "
                >
                  <div className="border-b border-panelline p-4">
                    <p className="truncate text-sm font-semibold text-ink2">
                      {displayName}
                    </p>

                    <p className="mt-1 truncate text-xs text-muted">
                      {email}
                    </p>
                  </div>

                  <div className="p-2">
                    <Link
                      to="/admin/settings"
                      onClick={() =>
                        setProfileOpen(
                          false,
                        )
                      }
                      className="
                        flex
                        items-center
                        gap-3
                        rounded-lg
                        px-3
                        py-2.5
                        text-xs
                        font-medium
                        text-muted
                        no-underline
                        hover:bg-white/[0.04]
                        hover:text-ink2
                      "
                    >
                      <span>
                        ⚙
                      </span>

                      Account Settings
                    </Link>

                    <button
                      type="button"
                      onClick={() => {
                        setProfileOpen(
                          false,
                        )
                        logout()
                      }}
                      className="
                        flex
                        w-full
                        items-center
                        gap-3
                        rounded-lg
                        px-3
                        py-2.5
                        text-left
                        text-xs
                        font-medium
                        text-red-400
                        hover:bg-red-500/[0.06]
                      "
                    >
                      <span>
                        ↪
                      </span>

                      Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* ==========================================================
            SCROLLABLE PAGE CONTENT
            ========================================================== */}

        <main
          className="
            min-h-0
            flex-1
            overflow-y-auto
            overflow-x-hidden
            bg-app
          "
        >
          <div
            className="
              mx-auto
              w-full
              max-w-[1600px]
              p-4
              sm:p-6
              lg:p-7
            "
          >
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
