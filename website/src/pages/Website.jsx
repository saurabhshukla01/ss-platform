import { useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import Tabs from '../components/Tabs'
import CrudManager from '../components/CrudManager'

const TABS = ['Banners', 'Announcements', 'Offers', 'Projects', 'Team', 'Testimonials']

export default function Website() {
  const [tab, setTab] = useState('Banners')

  return (
    <AdminLayout title="Website">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'Banners' && (
        <CrudManager
          base="/website/banners"
          fields={[
            { name: 'title', label: 'Title', required: true },
            { name: 'image_url', label: 'Image URL' },
            { name: 'link_url', label: 'Link URL' },
            { name: 'display_order', label: 'Display order', type: 'number' },
            { name: 'is_active', label: 'Active', type: 'checkbox' },
          ]}
          columns={[
            { key: 'title', label: 'Title' },
            { key: 'display_order', label: 'Order' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No banners yet — add one to show it in the Home page hero."
        />
      )}

      {tab === 'Announcements' && (
        <CrudManager
          base="/website/announcements"
          fields={[
            { name: 'message', label: 'Message', required: true },
            { name: 'link_url', label: 'Link URL' },
            { name: 'is_active', label: 'Active', type: 'checkbox' },
          ]}
          columns={[
            { key: 'message', label: 'Message' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No announcements yet — the site's announcement bar is empty."
        />
      )}

      {tab === 'Offers' && (
        <CrudManager
          base="/website/offers"
          fields={[
            { name: 'title', label: 'Title', required: true },
            { name: 'description', label: 'Description', type: 'textarea' },
            { name: 'discount_label', label: 'Discount label (e.g. "20% OFF")' },
            { name: 'is_active', label: 'Active', type: 'checkbox' },
          ]}
          columns={[
            { key: 'title', label: 'Title' },
            { key: 'discount_label', label: 'Discount' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No offers yet."
        />
      )}

      {tab === 'Projects' && (
        <CrudManager
          base="/website/projects"
          fields={[
            { name: 'title', label: 'Title', required: true },
            { name: 'slug', label: 'Slug', required: true },
            { name: 'summary', label: 'Summary', type: 'textarea' },
            { name: 'tech_stack', label: 'Tech stack (comma-separated)' },
            { name: 'live_url', label: 'Live URL' },
            { name: 'status', label: 'Status', type: 'select', options: ['live', 'completed'] },
            { name: 'is_featured', label: 'Featured', type: 'checkbox' },
          ]}
          columns={[
            { key: 'title', label: 'Title' },
            { key: 'status', label: 'Status' },
            { key: 'is_featured', label: 'Featured', render: (r) => (r.is_featured ? 'Yes' : 'No') },
          ]}
          emptyLabel="No projects yet — add your first case study."
        />
      )}

      {tab === 'Team' && (
        <CrudManager
          base="/website/team"
          fields={[
            { name: 'full_name', label: 'Full name', required: true },
            { name: 'role_title', label: 'Role' },
            { name: 'bio', label: 'Bio', type: 'textarea' },
            { name: 'photo_url', label: 'Photo URL' },
          ]}
          columns={[
            { key: 'full_name', label: 'Name' },
            { key: 'role_title', label: 'Role' },
          ]}
          emptyLabel="No team members listed yet."
        />
      )}

      {tab === 'Testimonials' && (
        <CrudManager
          base="/website/testimonials"
          fields={[
            { name: 'client_name', label: 'Client name', required: true },
            { name: 'client_company', label: 'Company' },
            { name: 'quote', label: 'Quote', type: 'textarea', required: true },
            { name: 'rating', label: 'Rating (1-5)', type: 'number' },
          ]}
          columns={[
            { key: 'client_name', label: 'Client' },
            { key: 'client_company', label: 'Company' },
            { key: 'rating', label: 'Rating' },
          ]}
          emptyLabel="No testimonials yet."
        />
      )}
    </AdminLayout>
  )
}
