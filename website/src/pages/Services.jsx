import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import ServiceCard from '../components/ServiceCard'
import api from '../api/client'
import { services as fallbackServices, categories as fallbackCategories } from '../data/placeholder'

export default function Services() {
  const [services, setServices] = useState(fallbackServices)
  const [categories, setCategories] = useState(fallbackCategories)
  const [activeCategory, setActiveCategory] = useState('all')

  useEffect(() => {
    api.get('/services').then((res) => {
      if (res.data?.length) {
        setServices(res.data.map((s) => ({ ...s, category: s.category?.name, category_slug: s.category?.slug })))
      }
    }).catch(() => {})
  }, [])

  const filtered = activeCategory === 'all'
    ? services
    : services.filter((s) => (s.category_slug || s.category?.toLowerCase().replace(/\s+/g, '-')) === activeCategory)

  return (
    <Layout>
      <section className="container-page pt-16 pb-10">
        <p className="label-eyebrow mb-4">Services</p>
        <h1 className="text-4xl md:text-5xl font-semibold text-high max-w-2xl">
          One catalogue, every stage of the stack.
        </h1>
        <p className="text-muted mt-4 max-w-xl">
          Digital products, applications, infrastructure and business solutions —
          managed and priced from the Admin Panel.
        </p>
      </section>

      <section className="container-page pb-6">
        <div className="flex flex-wrap gap-2">
          <FilterButton active={activeCategory === 'all'} onClick={() => setActiveCategory('all')}>
            All
          </FilterButton>
          {categories.map((c) => (
            <FilterButton key={c.slug} active={activeCategory === c.slug} onClick={() => setActiveCategory(c.slug)}>
              {c.name}
            </FilterButton>
          ))}
        </div>
      </section>

      <section className="container-page pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((s) => <ServiceCard key={s.slug} service={s} />)}
        </div>
        {filtered.length === 0 && (
          <p className="text-muted text-sm">No services listed in this category yet.</p>
        )}
      </section>
    </Layout>
  )
}

function FilterButton({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      className={`text-sm px-4 py-2 rounded border transition-colors ${
        active ? 'border-electric text-electric' : 'border-line text-muted hover:text-high'
      }`}
    >
      {children}
    </button>
  )
}
