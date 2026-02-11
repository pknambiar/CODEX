from datetime import date


def test_create_job_success(client):
    payload = {
        "company_name": "Acme Corp",
        "role_title": "Chief Operating Officer",
        "location": "New York",
        "compensation_band": "$250k-$350k",
        "source": "LinkedIn",
        "application_status": "Identified",
        "notes": "Strong fit",
    }
    response = client.post("/jobs", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["company_name"] == "Acme Corp"
    assert body["id"]


def test_prevent_duplicate_job_entry(client):
    payload = {
        "company_name": "Globex",
        "role_title": "Chief Strategy Officer",
        "location": "Remote",
        "compensation_band": "$220k-$300k",
        "source": "Recruiter",
        "application_status": "Applied",
        "notes": None,
    }
    assert client.post("/jobs", json=payload).status_code == 201
    duplicate_response = client.post("/jobs", json=payload)
    assert duplicate_response.status_code == 409


def test_add_outreach_record(client):
    job_payload = {
        "company_name": "Initech",
        "role_title": "VP Operations",
        "location": "Austin",
        "compensation_band": "$180k-$240k",
        "source": "Referral",
        "application_status": "Recruiter Contacted",
        "notes": "Warm intro",
    }
    job = client.post("/jobs", json=job_payload).json()

    outreach_payload = {
        "job_id": job["id"],
        "contact_name": "Jane Smith",
        "contact_designation": "Partner",
        "channel": "Email",
        "outreach_date": str(date.today()),
        "response_status": "Responded",
        "follow_up_date": str(date.today()),
        "notes": "Promising",
    }
    response = client.post("/outreach", json=outreach_payload)
    assert response.status_code == 201
    assert response.json()["job_id"] == job["id"]


def test_retrieve_dashboard_metrics(client):
    jobs = [
        {
            "company_name": "Alpha",
            "role_title": "COO",
            "location": "NY",
            "compensation_band": "$300k+",
            "source": "LinkedIn",
            "application_status": "Identified",
            "notes": "",
        },
        {
            "company_name": "Beta",
            "role_title": "CEO",
            "location": "SF",
            "compensation_band": "$500k+",
            "source": "Referral",
            "application_status": "Applied",
            "notes": "",
        },
    ]
    for payload in jobs:
        client.post("/jobs", json=payload)

    response = client.get("/dashboard/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["total_opportunities"] == 2
    assert len(body["opportunities_by_stage"]) >= 2


def test_validate_incorrect_input_rejection(client):
    bad_payload = {
        "company_name": "A",
        "role_title": "COO",
        "location": "NY",
        "source": "LinkedIn",
        "application_status": "Identified",
    }
    response = client.post("/jobs", json=bad_payload)
    assert response.status_code == 422
