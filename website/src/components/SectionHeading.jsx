export default function SectionHeading({ eyebrow, title, description, light = false }) {
  return (
    <div className="max-w-2xl">
      {eyebrow && <p className="label-eyebrow mb-3">{eyebrow}</p>}
      <h2 className={`text-3xl md:text-4xl font-semibold ${light ? 'text-ink' : 'text-high'}`}>{title}</h2>
      {description && (
        <p className={`mt-4 text-base leading-relaxed ${light ? 'text-muted2' : 'text-muted'}`}>{description}</p>
      )}
    </div>
  )
}
