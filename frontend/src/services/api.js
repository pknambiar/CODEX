import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
})

export const listJobs = () => api.get('/jobs')
export const createJob = (payload) => api.post('/jobs', payload)
export const getMetrics = () => api.get('/dashboard/metrics')

export default api
