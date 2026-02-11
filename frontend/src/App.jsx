import { useEffect, useState } from 'react'
import DashboardCharts from './components/DashboardCharts'
import JobForm from './components/JobForm'
import JobTable from './components/JobTable'
import { createJob, getMetrics, listJobs } from './services/api'

export default function App() {
  const [jobs, setJobs] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [error, setError] = useState('')

  const loadData = async () => {
    try {
      const [jobsResponse, metricsResponse] = await Promise.all([listJobs(), getMetrics()])
      setJobs(jobsResponse.data)
      setMetrics(metricsResponse.data)
      setError('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard data')
    }
  }

  const handleCreateJob = async (payload) => {
    try {
      await createJob(payload)
      await loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to create job')
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  return (
    <div className="container">
      <header>
        <h1>Executive Job Search Intelligence Dashboard</h1>
      </header>
      {error && <p className="error">{error}</p>}
      <JobForm onSubmit={handleCreateJob} />
      <JobTable jobs={jobs} />
      {metrics && <DashboardCharts metrics={metrics} />}
    </div>
  )
}
