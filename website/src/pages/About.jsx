import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import SectionHeading from '../components/SectionHeading'
import { Link } from 'react-router-dom'
import api from '../api/client'

export default function About() {
  const [team, setTeam] = useState([])

  useEffect(() => {
    api.get('/website/team').then((res) => setTeam(res.data || [])).catch(() => {})
  }, [])

  return (
    <Layout>
      <section className="container-page pt-16 pb-20">
        <p className="label-eyebrow mb-4">About</p>
        <h1 className="text-4xl md:text-5xl font-semibold text-high max-w-2xl leading-tight">
          Technology built by someone who runs a business, not just a dev shop.
        </h1>
        <p className="text-muted mt-6 max-w-2xl leading-relaxed">
          Saurabh Shukla is the CTO of SS Collections Group and the person behind this
          platform. The work here isn't built as a portfolio piece — it's the same
          approach used to run a real company: services need transparent pricing,
          inquiries need to become tracked leads, and content needs to be editable
          without touching code.
        </p>
      </section>

      <section className="container-page py-16 border-t border-line grid md:grid-cols-2 gap-12">
        <div>
          <h2 className="text-2xl font-semibold text-high">Working approach</h2>
          <ul className="mt-6 space-y-5">
            {[
              ['Understand the business first', 'Every build starts with the services, prices and workflows you actually run — not a generic template.'],
              ['Ship an Admin Panel, not just a website', 'Services, pricing, offers and content should be editable without a developer.'],
              ['Design for handover', 'Documented APIs, migration history and clear audit logs — the platform is yours to run.'],
            ].map(([title, body]) => (
              <li key={title} className="border-l-2 border-electric pl-4">
                <p className="text-high font-medium">{title}</p>
                <p className="text-muted text-sm mt-1 leading-relaxed">{body}</p>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="text-2xl font-semibold text-high">Expertise</h2>
          <div className="mt-6 flex flex-wrap gap-2">
            {['React', 'Vite', 'FastAPI', 'Python', 'MySQL', 'SQLAlchemy', 'JWT Auth', 'Nginx', 'Cloud Deployment', 'REST APIs', 'CRM Design', 'SEO'].map((t) => (
              <span key={t} className="text-sm border border-line rounded px-3 py-1.5 text-muted">{t}</span>
            ))}
          </div>

          <div className="mt-10 card-dark">
            <p className="text-high font-medium">CTO — SS Collections Group</p>
            <p className="text-muted text-sm mt-2 leading-relaxed">
              Leading technology strategy and platform development for SS Collections
              Group, and building the same services for outside clients through this
              platform.
            </p>
          </div>

          {team.length > 0 && (
            <div className="mt-10 space-y-4">
              {team.map((member) => (
                <div key={member.id} className="border-l-2 border-electric pl-4">
                  <p className="text-high font-medium">{member.full_name}</p>
                  {member.role_title && <p className="text-muted2 text-xs">{member.role_title}</p>}
                  {member.bio && <p className="text-muted text-sm mt-1 leading-relaxed">{member.bio}</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="container-page py-16 border-t border-line">
        <SectionHeading title="Have a project in mind?" />
        <Link to="/inquiry" className="btn-primary mt-6 inline-flex">Start a conversation</Link>
      </section>
    </Layout>
  )
}
