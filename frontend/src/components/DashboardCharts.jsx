import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#7C4DFF', '#2E7D32']

export default function DashboardCharts({ metrics }) {
  return (
    <section className="card charts">
      <h2>Pipeline Metrics</h2>
      <div className="chart-grid">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={metrics.opportunities_by_stage}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="stage" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#1f77b4" />
          </BarChart>
        </ResponsiveContainer>

        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Tooltip />
            <Legend />
            <Pie data={metrics.source_effectiveness} dataKey="count" nameKey="source" outerRadius={100} label>
              {metrics.source_effectiveness.map((entry, index) => (
                <Cell key={entry.source} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={metrics.monthly_additions}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#16a085" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
