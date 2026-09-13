import { useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import Tabs from '../components/Tabs'
import CrudManager from '../components/CrudManager'

const TABS = ['Page Meta', 'Redirects']

export default function SEO() {
  const [tab, setTab] = useState('Page Meta')

  return (
    <AdminLayout title="SEO">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'Page Meta' && (
        <CrudManager
          base="/seo/meta"
          fields={[
            { name: 'path', label: 'Path (e.g. /services/website-development)', required: true },
            { name: 'title', label: 'Title' },
            { name: 'description', label: 'Description', type: 'textarea' },
            { name: 'canonical_url', label: 'Canonical URL' },
            { name: 'og_image_url', label: 'OG image URL' },
          ]}
          columns={[
            { key: 'path', label: 'Path' },
            { key: 'title', label: 'Title' },
          ]}
          emptyLabel="No per-page SEO overrides yet."
        />
      )}

      {tab === 'Redirects' && (
        <CrudManager
          base="/seo/redirects"
          fields={[
            { name: 'from_path', label: 'From path', required: true },
            { name: 'to_path', label: 'To path', required: true },
            { name: 'status_code', label: 'Status code', type: 'number' },
            { name: 'is_active', label: 'Active', type: 'checkbox' },
          ]}
          columns={[
            { key: 'from_path', label: 'From' },
            { key: 'to_path', label: 'To' },
            { key: 'status_code', label: 'Code' },
          ]}
          emptyLabel="No redirects configured yet."
        />
      )}
    </AdminLayout>
  )
}
