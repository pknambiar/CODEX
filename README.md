# Executive Job Search Intelligence Dashboard

A production-oriented full-stack dashboard for executives to track job opportunities, outreach pipeline, recruiter interactions, and funnel metrics with optional AI-assisted outreach drafts.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic, pytest
- **Frontend**: React (Vite), Axios, Recharts
- **Database**: SQLite (local default), PostgreSQL-ready via `DATABASE_URL`
- **Containerization**: Docker + docker-compose

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   └── tests/
├── requirements.txt
├── .env.example
└── Dockerfile

frontend/
└── src/
    ├── components/
    ├── services/
    └── ...
```

## Local Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI is available at `http://localhost:5173`, API at `http://localhost:8000`.

## Docker Setup

Run full stack with:

```bash
docker-compose up --build
```

## Environment Variables

Defined in `backend/.env.example`:

- `DATABASE_URL`: SQLAlchemy database URL
- `OPENAI_API_KEY`: Optional key to enable real AI-provider mode
- `ALLOWED_ORIGINS`: CORS allowlist (comma-separated)
- `APP_NAME`: FastAPI app title

## API Endpoints

### Health
- `GET /health`

### Jobs
- `POST /jobs`
- `GET /jobs?status=Applied&skip=0&limit=20&sort_order=desc`
- `GET /jobs/{job_id}`
- `PUT /jobs/{job_id}`
- `DELETE /jobs/{job_id}`

### Outreach
- `POST /outreach`
- `GET /outreach/job/{job_id}`

### Dashboard
- `GET /dashboard/metrics`

### AI
- `POST /ai/generate-outreach`

## Sample cURL Commands

Create a job:

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "role_title": "Chief Operating Officer",
    "location": "New York",
    "compensation_band": "$250k-$350k",
    "source": "LinkedIn",
    "application_status": "Identified",
    "notes": "Priority role"
  }'
```

Create outreach:

```bash
curl -X POST http://localhost:8000/outreach \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "<job_uuid>",
    "contact_name": "Jane Smith",
    "contact_designation": "Managing Partner",
    "channel": "Email",
    "outreach_date": "2026-01-15",
    "response_status": "Responded",
    "follow_up_date": "2026-01-20",
    "notes": "Requested profile"
  }'
```

Retrieve metrics:

```bash
curl http://localhost:8000/dashboard/metrics
```

Generate outreach draft:

```bash
curl -X POST http://localhost:8000/ai/generate-outreach \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "role_title": "Chief Operating Officer",
    "value_proposition": "leading operational turnarounds and scaling cross-functional execution"
  }'
```

## Testing

Backend tests:

```bash
cd backend
pytest
```

Includes tests for:
- successful job creation
- duplicate prevention
- outreach creation
- dashboard metrics retrieval
- invalid input validation
