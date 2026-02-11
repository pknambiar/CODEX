export default function JobTable({ jobs }) {
  return (
    <section className="card">
      <h2>Opportunities</h2>
      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Role</th>
            <th>Status</th>
            <th>Source</th>
            <th>Date Added</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id}>
              <td>{job.company_name}</td>
              <td>{job.role_title}</td>
              <td>{job.application_status}</td>
              <td>{job.source}</td>
              <td>{new Date(job.date_added).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
