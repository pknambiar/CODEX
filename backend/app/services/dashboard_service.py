from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ApplicationStatus, JobOpportunity
from app.schemas.dashboard import DashboardMetrics, MonthlyMetric, SourceMetric, StageMetric

STAGE_FLOW = [
    ApplicationStatus.IDENTIFIED.value,
    ApplicationStatus.APPLIED.value,
    ApplicationStatus.RECRUITER_CONTACTED.value,
    ApplicationStatus.INTERVIEW_STAGE.value,
    ApplicationStatus.OFFER.value,
    ApplicationStatus.CLOSED.value,
]


def _safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def get_metrics(db: Session) -> DashboardMetrics:
    jobs = db.query(JobOpportunity).all()
    total = len(jobs)

    by_stage = defaultdict(int)
    by_source = defaultdict(int)
    monthly = defaultdict(int)
    days_in_stage = defaultdict(list)

    now = datetime.utcnow()
    for job in jobs:
        stage = job.application_status.value
        by_stage[stage] += 1
        by_source[job.source.value] += 1
        monthly[job.date_added.strftime("%Y-%m")] += 1

        baseline = job.last_updated or job.date_added
        days_in_stage[stage].append(max((now - baseline).days, 0))

    stage_metrics = [StageMetric(stage=stage, count=by_stage.get(stage, 0)) for stage in STAGE_FLOW]
    source_metrics = [SourceMetric(source=src, count=count) for src, count in sorted(by_source.items())]
    monthly_metrics = [MonthlyMetric(month=month, count=count) for month, count in sorted(monthly.items())]

    conversion = {}
    for idx in range(len(STAGE_FLOW) - 1):
        current_stage = STAGE_FLOW[idx]
        next_stage = STAGE_FLOW[idx + 1]
        key = f"{current_stage} -> {next_stage}"
        conversion[key] = _safe_rate(by_stage.get(next_stage, 0), by_stage.get(current_stage, 0))

    average_days = {
        stage: round(sum(days) / len(days), 2) if days else 0.0 for stage, days in days_in_stage.items()
    }

    return DashboardMetrics(
        total_opportunities=total,
        opportunities_by_stage=stage_metrics,
        conversion_rates=conversion,
        average_days_in_stage=average_days,
        source_effectiveness=source_metrics,
        monthly_additions=monthly_metrics,
    )
