import Layout from '../components/Layout'
import { projects } from '../data/placeholder'

export default function Projects() {
  return (
    <Layout>
      <section className="container-page pt-16 pb-10">
        <p className="label-eyebrow mb-3">Projects</p>
        <h1 className="text-4xl md:text-5xl font-semibold text-high max-w-2xl">
          Live and completed work.
        </h1>
      </section>

      <section className="container-page pb-24 grid md:grid-cols-2 gap-6">
        {projects.map((p) => (
          <article key={p.title} className="card-dark">
            <p className="text-xs text-cyan mb-2">{p.status === 'live' ? 'Live' : 'Completed'}</p>
            <h2 className="text-xl font-medium text-high">{p.title}</h2>
            <p className="text-muted mt-2 leading-relaxed">{p.summary}</p>
            <p className="text-xs text-muted2 mt-6 pt-4 border-t border-line">{p.stack}</p>
          </article>
        ))}
      </section>
    </Layout>
  )
}
