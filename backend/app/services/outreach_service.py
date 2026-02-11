from sqlalchemy.orm import Session

from app.models import OutreachRecord
from app.schemas.outreach import OutreachCreate
from app.services.job_service import JobNotFoundError, get_job_or_404


def create_outreach(db: Session, payload: OutreachCreate) -> OutreachRecord:
    try:
        get_job_or_404(db, payload.job_id)
    except JobNotFoundError as exc:
        raise JobNotFoundError("Referenced job does not exist") from exc

    outreach = OutreachRecord(**payload.model_dump())
    db.add(outreach)
    db.commit()
    db.refresh(outreach)
    return outreach


def list_outreach_by_job(db: Session, job_id: str) -> list[OutreachRecord]:
    get_job_or_404(db, job_id)
    return db.query(OutreachRecord).filter(OutreachRecord.job_id == job_id).all()
