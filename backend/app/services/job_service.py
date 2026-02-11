from datetime import datetime

from sqlalchemy import asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import JobOpportunity
from app.schemas.job import JobCreate, JobUpdate


class DuplicateJobError(Exception):
    pass


class JobNotFoundError(Exception):
    pass


def create_job(db: Session, payload: JobCreate) -> JobOpportunity:
    job = JobOpportunity(**payload.model_dump())
    db.add(job)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateJobError("Job with this company and role already exists") from exc
    db.refresh(job)
    return job


def list_jobs(
    db: Session,
    status: str | None = None,
    skip: int = 0,
    limit: int = 20,
    sort_order: str = "desc",
) -> list[JobOpportunity]:
    query = select(JobOpportunity)
    if status:
        query = query.where(JobOpportunity.application_status == status)
    order_fn = desc if sort_order.lower() == "desc" else asc
    query = query.order_by(order_fn(JobOpportunity.date_added)).offset(skip).limit(limit)
    return list(db.scalars(query).all())


def get_job_or_404(db: Session, job_id: str) -> JobOpportunity:
    job = db.get(JobOpportunity, job_id)
    if not job:
        raise JobNotFoundError("Job not found")
    return job


def update_job(db: Session, job_id: str, payload: JobUpdate) -> JobOpportunity:
    job = get_job_or_404(db, job_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, key, value)
    job.last_updated = datetime.utcnow()
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateJobError("Job with this company and role already exists") from exc
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: str) -> None:
    job = get_job_or_404(db, job_id)
    db.delete(job)
    db.commit()
