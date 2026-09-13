import { Link } from 'react-router-dom'
import Layout from '../components/Layout'

export default function NotFound() {
  return (
    <Layout>
      <section className="container-page py-32 text-center">
        <p className="text-electric font-display text-5xl font-semibold">404</p>
        <p className="text-muted mt-4">This page doesn't exist.</p>
        <Link to="/" className="btn-primary mt-8 inline-flex">Back to home</Link>
      </section>
    </Layout>
  )
}
