import { useState } from 'react'

const initialState = {
  company_name: '',
  role_title: '',
  location: '',
  compensation_band: '',
  source: 'LinkedIn',
  application_status: 'Identified',
  notes: '',
}

export default function JobForm({ onSubmit }) {
  const [form, setForm] = useState(initialState)

  const updateField = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    await onSubmit(form)
    setForm(initialState)
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Add Opportunity</h2>
      <div className="grid">
        <input name="company_name" placeholder="Company" value={form.company_name} onChange={updateField} required />
        <input name="role_title" placeholder="Role" value={form.role_title} onChange={updateField} required />
        <input name="location" placeholder="Location" value={form.location} onChange={updateField} required />
        <input
          name="compensation_band"
          placeholder="Compensation Band"
          value={form.compensation_band}
          onChange={updateField}
        />
        <select name="source" value={form.source} onChange={updateField}>
          <option>LinkedIn</option>
          <option>Recruiter</option>
          <option>Referral</option>
          <option>Search Firm</option>
        </select>
        <select name="application_status" value={form.application_status} onChange={updateField}>
          <option>Identified</option>
          <option>Applied</option>
          <option>Recruiter Contacted</option>
          <option>Interview Stage</option>
          <option>Offer</option>
          <option>Closed</option>
        </select>
      </div>
      <textarea name="notes" placeholder="Notes" value={form.notes} onChange={updateField} rows={3} />
      <button type="submit">Create Opportunity</button>
    </form>
  )
}
