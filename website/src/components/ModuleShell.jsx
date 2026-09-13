export default function ModuleShell({ title, description, tableColumns = [] }) {
  return (
    <div className="panel p-8 text-center max-w-2xl mx-auto mt-6">
      <h2 className="text-lg font-semibold text-ink2">{title}</h2>
      <p className="text-sm text-muted mt-2 leading-relaxed">{description}</p>
      {tableColumns.length > 0 && (
        <div className="mt-6 border border-panelline rounded overflow-hidden text-left">
          <table className="w-full">
            <thead>
              <tr className="bg-canvas">
                {tableColumns.map((c) => <th key={c} className="th">{c}</th>)}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td colSpan={tableColumns.length} className="td text-center text-muted2 py-8">
                  No data yet — this module's table exists in the database and is ready to be connected.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
