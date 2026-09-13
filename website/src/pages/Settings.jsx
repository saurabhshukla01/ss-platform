import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import { useAuth } from '../auth/AuthContext'
import api from '../api/client'

/*
|--------------------------------------------------------------------------
| Settings Groups
|--------------------------------------------------------------------------
*/

const GROUPS = [
  {
    key: 'company',
    label: 'Company',
    description:
      'Manage your company identity, contact information and public business details.',
    icon: '🏢',
    color: 'cyan',
    fields: [
      {
        key: 'name',
        label: 'Company Name',
        placeholder: 'SS Platform',
      },
      {
        key: 'email',
        label: 'Business Email',
        type: 'email',
        placeholder: 'hello@example.com',
      },
      {
        key: 'phone',
        label: 'Phone Number',
        placeholder: '+91 98765 43210',
      },
      {
        key: 'address',
        label: 'Business Address',
        placeholder: 'Enter your business address',
      },
    ],
  },

  {
    key: 'smtp',
    label: 'SMTP',
    description:
      'Configure outgoing email used for contact forms, inquiries and notifications.',
    icon: '✉️',
    color: 'purple',
    fields: [
      {
        key: 'host',
        label: 'SMTP Host',
        placeholder: 'smtp.gmail.com',
      },
      {
        key: 'port',
        label: 'SMTP Port',
        placeholder: '587',
      },
      {
        key: 'username',
        label: 'SMTP Username',
        placeholder: 'your-email@example.com',
      },
      {
        key: 'password',
        label: 'SMTP Password',
        type: 'password',
        secret: true,
        placeholder: 'Enter SMTP password',
      },
    ],
  },

  {
    key: 'payment',
    label: 'Payment',
    description:
      'Manage payment gateway configuration, API keys and webhook security.',
    icon: '💳',
    color: 'green',
    fields: [
      {
        key: 'gateway',
        label: 'Payment Gateway',
        placeholder: 'razorpay / stripe / demo',
      },
      {
        key: 'key_id',
        label: 'Gateway Key ID',
        placeholder: 'Enter gateway key ID',
      },
      {
        key: 'key_secret',
        label: 'Gateway Secret',
        type: 'password',
        secret: true,
        placeholder: 'Enter gateway secret',
      },
      {
        key: 'webhook_secret',
        label: 'Webhook Secret',
        type: 'password',
        secret: true,
        placeholder: 'Enter webhook secret',
      },
    ],
  },

  {
    key: 'tracking',
    label: 'Tracking',
    description:
      'Configure analytics defaults and tracking information used by your website.',
    icon: '📊',
    color: 'orange',
    fields: [
      {
        key: 'default_utm_source',
        label: 'Default UTM Source',
        placeholder: 'website',
      },
    ],
  },

  {
    key: 'security',
    label: 'Security',
    description:
      'Configure session duration and administrator access restrictions.',
    icon: '🔐',
    color: 'red',
    fields: [
      {
        key: 'session_minutes',
        label: 'Session Duration',
        placeholder: '120',
        suffix: 'minutes',
      },
      {
        key: 'ip_allowlist',
        label: 'IP Allowlist',
        placeholder:
          '192.168.1.1, 10.0.0.1',
      },
    ],
  },
]

/*
|--------------------------------------------------------------------------
| Main Settings Page
|--------------------------------------------------------------------------
*/

export default function Settings() {
  const { admin } = useAuth()

  return (
    <AdminLayout title="Settings">
      <div className="space-y-6">

        {/* ============================================================
            PAGE HEADER
            ============================================================ */}

        <div
          className="
            relative
            overflow-hidden
            rounded-2xl
            border
            border-panelline
            bg-gradient-to-br
            from-panel
            via-panel
            to-slate-900/80
            p-6
            shadow-sm
          "
        >
          <div
            className="
              absolute
              -right-20
              -top-20
              h-48
              w-48
              rounded-full
              bg-cyan-400/10
              blur-3xl
            "
          />

          <div
            className="
              absolute
              -bottom-24
              right-32
              h-48
              w-48
              rounded-full
              bg-purple-500/10
              blur-3xl
            "
          />

          <div className="relative flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="mb-2 flex items-center gap-2">
                <span
                  className="
                    inline-flex
                    h-9
                    w-9
                    items-center
                    justify-center
                    rounded-xl
                    bg-cyan-400/10
                    text-lg
                  "
                >
                  ⚙️
                </span>

                <span
                  className="
                    text-xs
                    font-semibold
                    uppercase
                    tracking-[0.18em]
                    text-cyan-400
                  "
                >
                  Administration
                </span>
              </div>

              <h1
                className="
                  text-2xl
                  font-bold
                  tracking-tight
                  text-ink2
                  md:text-3xl
                "
              >
                Platform Settings
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
                Manage your company information, email,
                payments, tracking and security configuration
                from one central location.
              </p>
            </div>

            <div
              className="
                inline-flex
                w-fit
                items-center
                gap-2
                rounded-full
                border
                border-emerald-500/20
                bg-emerald-500/10
                px-3
                py-2
                text-xs
                font-medium
                text-emerald-400
              "
            >
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              System Configuration
            </div>
          </div>
        </div>

        {/* ============================================================
            ACCOUNT CARD
            ============================================================ */}

        <AccountCard admin={admin} />

        {/* ============================================================
            SETTINGS GRID
            ============================================================ */}

        <div>
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-ink2">
              Configuration
            </h2>

            <p className="mt-1 text-sm text-muted">
              Update the configuration used by your platform.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
            {GROUPS.map((group) => (
              <SettingsGroup
                key={group.key}
                group={group}
              />
            ))}
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}

/*
|--------------------------------------------------------------------------
| Account Card
|--------------------------------------------------------------------------
*/

function AccountCard({ admin }) {
  const initials =
    admin?.full_name
      ?.split(' ')
      .filter(Boolean)
      .map((word) => word[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() ||
    admin?.name
      ?.split(' ')
      .filter(Boolean)
      .map((word) => word[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() ||
    'AD'

  return (
    <div
      className="
        panel
        overflow-hidden
        rounded-2xl
      "
    >
      <div
        className="
          border-b
          border-panelline
          bg-gradient-to-r
          from-cyan-400/[0.06]
          via-transparent
          to-purple-500/[0.05]
          px-5
          py-4
        "
      >
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-sm font-semibold text-ink2">
              Your Account
            </h2>

            <p className="mt-1 text-xs text-muted">
              Administrator profile currently signed in.
            </p>
          </div>

          <div
            className="
              hidden
              rounded-full
              border
              border-cyan-400/20
              bg-cyan-400/10
              px-3
              py-1.5
              text-[11px]
              font-medium
              text-cyan-400
              sm:block
            "
          >
            Administrator
          </div>
        </div>
      </div>

      <div className="p-5">
        <div className="flex flex-col gap-5 md:flex-row md:items-center">
          {/* Avatar */}

          <div
            className="
              flex
              h-16
              w-16
              shrink-0
              items-center
              justify-center
              rounded-2xl
              bg-gradient-to-br
              from-cyan-400
              to-blue-600
              text-xl
              font-bold
              text-white
              shadow-lg
              shadow-cyan-500/10
            "
          >
            {initials}
          </div>

          {/* Name */}

          <div className="min-w-0 flex-1">
            <h3 className="truncate text-base font-semibold text-ink2">
              {admin?.full_name ||
                admin?.name ||
                'Administrator'}
            </h3>

            <p className="mt-1 truncate text-sm text-muted">
              {admin?.email || 'No email available'}
            </p>

            <div className="mt-3 flex flex-wrap gap-2">
              <span
                className="
                  rounded-full
                  bg-cyan-400/10
                  px-2.5
                  py-1
                  text-[10px]
                  font-semibold
                  uppercase
                  tracking-wide
                  text-cyan-400
                "
              >
                {admin?.role_name ||
                  admin?.role ||
                  'Admin'}
              </span>

              <span
                className="
                  rounded-full
                  bg-emerald-400/10
                  px-2.5
                  py-1
                  text-[10px]
                  font-semibold
                  uppercase
                  tracking-wide
                  text-emerald-400
                "
              >
                Active
              </span>
            </div>
          </div>

          {/* Details */}

          <div
            className="
              grid
              grid-cols-2
              gap-3
              md:min-w-[270px]
            "
          >
            <AccountStat
              label="Account"
              value="Active"
            />

            <AccountStat
              label="Access"
              value={
                admin?.role_name ||
                admin?.role ||
                'Admin'
              }
            />
          </div>
        </div>
      </div>
    </div>
  )
}

/*
|--------------------------------------------------------------------------
| Account Stat
|--------------------------------------------------------------------------
*/

function AccountStat({ label, value }) {
  return (
    <div
      className="
        rounded-xl
        border
        border-panelline
        bg-black/[0.02]
        px-4
        py-3
      "
    >
      <p className="text-[10px] font-medium uppercase tracking-wider text-muted">
        {label}
      </p>

      <p className="mt-1 truncate text-xs font-semibold text-ink2">
        {value}
      </p>
    </div>
  )
}

/*
|--------------------------------------------------------------------------
| Settings Group
|--------------------------------------------------------------------------
*/

function SettingsGroup({ group }) {
  const [values, setValues] =
    useState({})

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  const [savingField, setSavingField] =
    useState(null)

  const [savedField, setSavedField] =
    useState(null)

  const [visibleSecrets, setVisibleSecrets] =
    useState({})

  /*
  |--------------------------------------------------------------------------
  | Load Settings
  |--------------------------------------------------------------------------
  */

  useEffect(() => {
    let mounted = true

    async function loadSettings() {
      setLoading(true)
      setError('')

      try {
        const response = await api.get(
          '/settings',
          {
            params: {
              group: group.key,
            },
          },
        )

        if (!mounted) return

        const settings =
          Array.isArray(response.data)
            ? response.data
            : []

        const loadedValues = {}

        settings.forEach((setting) => {
          loadedValues[setting.key] =
            setting.value ?? ''
        })

        setValues(loadedValues)
      } catch (err) {
        console.error(
          `Failed to load ${group.key} settings:`,
          err,
        )

        if (mounted) {
          setError(
            getApiError(
              err,
              'Unable to load settings.',
            ),
          )
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadSettings()

    return () => {
      mounted = false
    }
  }, [group.key])

  /*
  |--------------------------------------------------------------------------
  | Handle Change
  |--------------------------------------------------------------------------
  */

  function handleChange(
    field,
    value,
  ) {
    setValues((current) => ({
      ...current,
      [field]: value,
    }))

    setSavedField(null)
  }

  /*
  |--------------------------------------------------------------------------
  | Toggle Secret
  |--------------------------------------------------------------------------
  */

  function toggleSecret(field) {
    setVisibleSecrets(
      (current) => ({
        ...current,
        [field]:
          !current[field],
      }),
    )
  }

  /*
  |--------------------------------------------------------------------------
  | Save
  |--------------------------------------------------------------------------
  */

  async function save(field) {
    setSavingField(field)
    setError('')
    setSavedField(null)

    try {
      await api.put(
        '/settings',
        {
          group: group.key,
          key: field,
          value:
            values[field] ?? '',
          is_secret:
            group.fields.find(
              (item) =>
                item.key === field,
            )?.secret || false,
        },
      )

      setSavedField(field)

      window.setTimeout(() => {
        setSavedField(
          (current) =>
            current === field
              ? null
              : current,
        )
      }, 2500)
    } catch (err) {
      console.error(
        `Failed to save ${group.key}.${field}:`,
        err,
      )

      setError(
        getApiError(
          err,
          'Unable to save setting.',
        ),
      )
    } finally {
      setSavingField(null)
    }
  }

  /*
  |--------------------------------------------------------------------------
  | Render
  |--------------------------------------------------------------------------
  */

  return (
    <section
      className="
        panel
        overflow-hidden
        rounded-2xl
        transition
        duration-200
        hover:border-cyan-400/20
      "
    >
      {/* ==========================================================
          GROUP HEADER
          ========================================================== */}

      <div className="border-b border-panelline p-5">
        <div className="flex items-start gap-4">
          {/* Icon */}

          <div
            className={`
              flex
              h-11
              w-11
              shrink-0
              items-center
              justify-center
              rounded-xl
              text-lg
              ${getIconBackground(
                group.color,
              )}
            `}
          >
            {group.icon}
          </div>

          {/* Text */}

          <div className="min-w-0 flex-1">
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-sm font-semibold text-ink2">
                {group.label}
              </h3>

              {!loading && !error && (
                <span
                  className="
                    rounded-full
                    bg-emerald-400/10
                    px-2
                    py-1
                    text-[9px]
                    font-semibold
                    uppercase
                    tracking-wider
                    text-emerald-400
                  "
                >
                  Ready
                </span>
              )}
            </div>

            <p className="mt-1 text-xs leading-5 text-muted">
              {group.description}
            </p>
          </div>
        </div>
      </div>

      {/* ==========================================================
          BODY
          ========================================================== */}

      <div className="p-5">
        {/* Loading */}

        {loading ? (
          <SettingsSkeleton />
        ) : (
          <div className="space-y-4">
            {group.fields.map(
              (field) => (
                <SettingField
                  key={field.key}
                  field={field}
                  value={
                    values[field.key] ||
                    ''
                  }
                  visible={
                    visibleSecrets[
                      field.key
                    ]
                  }
                  saving={
                    savingField ===
                    field.key
                  }
                  saved={
                    savedField ===
                    field.key
                  }
                  onChange={
                    handleChange
                  }
                  onToggleSecret={
                    toggleSecret
                  }
                  onSave={save}
                />
              ),
            )}
          </div>
        )}

        {/* Error */}

        {error && (
          <div
            className="
              mt-4
              flex
              items-start
              gap-3
              rounded-xl
              border
              border-red-500/20
              bg-red-500/[0.06]
              p-3
            "
          >
            <span className="mt-0.5 text-sm">
              ⚠️
            </span>

            <div className="min-w-0">
              <p className="text-xs font-semibold text-red-400">
                Configuration Error
              </p>

              <p className="mt-1 text-[11px] leading-5 text-red-400/70">
                {error}
              </p>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

/*
|--------------------------------------------------------------------------
| Individual Setting Field
|--------------------------------------------------------------------------
*/

function SettingField({
  field,
  value,
  visible,
  saving,
  saved,
  onChange,
  onToggleSecret,
  onSave,
}) {
  const inputType =
    field.secret
      ? visible
        ? 'text'
        : 'password'
      : field.type || 'text'

  return (
    <div
      className="
        rounded-xl
        border
        border-panelline
        bg-black/[0.015]
        p-3
        transition
        duration-150
        focus-within:border-cyan-400/30
        focus-within:bg-cyan-400/[0.015]
      "
    >
      <div className="mb-2 flex items-center justify-between gap-3">
        <label
          className="
            text-[11px]
            font-semibold
            text-ink2
          "
        >
          {field.label}
        </label>

        {field.secret && (
          <span
            className="
              rounded-md
              bg-purple-400/10
              px-2
              py-1
              text-[9px]
              font-semibold
              uppercase
              tracking-wide
              text-purple-400
            "
          >
            Secret
          </span>
        )}
      </div>

      <div className="flex gap-2">
        <div className="relative min-w-0 flex-1">
          <input
            type={inputType}
            className="
              input
              w-full
              pr-10
              text-sm
            "
            value={value}
            placeholder={
              field.placeholder
            }
            onChange={(event) =>
              onChange(
                field.key,
                event.target.value,
              )
            }
            autoComplete={
              field.secret
                ? 'new-password'
                : 'off'
            }
          />

          {field.secret && (
            <button
              type="button"
              onClick={() =>
                onToggleSecret(
                  field.key,
                )
              }
              className="
                absolute
                right-2
                top-1/2
                -translate-y-1/2
                rounded-md
                p-1.5
                text-muted
                transition
                hover:bg-white/5
                hover:text-ink2
              "
              title={
                visible
                  ? 'Hide value'
                  : 'Show value'
              }
            >
              {visible
                ? '🙈'
                : '👁️'}
            </button>
          )}
        </div>

        {/* Save */}

        <button
          type="button"
          disabled={saving}
          onClick={() =>
            onSave(field.key)
          }
          className={`
            flex
            min-w-[76px]
            items-center
            justify-center
            gap-1.5
            rounded-lg
            px-3
            py-2
            text-[11px]
            font-semibold
            transition
            ${
              saved
                ? 'border border-emerald-400/20 bg-emerald-400/10 text-emerald-400'
                : 'btn-secondary'
            }
          `}
        >
          {saving ? (
            <>
              <span
                className="
                  h-3
                  w-3
                  animate-spin
                  rounded-full
                  border-2
                  border-current
                  border-t-transparent
                "
              />

              Saving
            </>
          ) : saved ? (
            <>
              ✓
              Saved
            </>
          ) : (
            <>
              Save
            </>
          )}
        </button>
      </div>

      {field.suffix && (
        <p className="mt-2 text-[10px] text-muted">
          Value is measured in {field.suffix}.
        </p>
      )}
    </div>
  )
}

/*
|--------------------------------------------------------------------------
| Loading Skeleton
|--------------------------------------------------------------------------
*/

function SettingsSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map(
        (item) => (
          <div
            key={item}
            className="
              animate-pulse
              rounded-xl
              border
              border-panelline
              p-3
            "
          >
            <div className="mb-2 h-3 w-28 rounded bg-white/5" />

            <div className="h-10 rounded-lg bg-white/5" />
          </div>
        ),
      )}
    </div>
  )
}

/*
|--------------------------------------------------------------------------
| Icon Background
|--------------------------------------------------------------------------
*/

function getIconBackground(color) {
  const backgrounds = {
    cyan:
      'bg-cyan-400/10',
    purple:
      'bg-purple-400/10',
    green:
      'bg-emerald-400/10',
    orange:
      'bg-orange-400/10',
    red:
      'bg-red-400/10',
  }

  return (
    backgrounds[color] ||
    backgrounds.cyan
  )
}

/*
|--------------------------------------------------------------------------
| API Error Helper
|--------------------------------------------------------------------------
*/

function getApiError(
  error,
  fallback,
) {
  const detail =
    error?.response?.data
      ?.detail

  if (
    typeof detail ===
    'string'
  ) {
    return detail
  }

  if (
    Array.isArray(detail)
  ) {
    return detail
      .map((item) =>
        item?.msg
          ? item.msg
          : String(item),
      )
      .join(', ')
  }

  if (
    error?.message
  ) {
    return error.message
  }

  return fallback
}
