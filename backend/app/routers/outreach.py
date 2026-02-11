from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.outreach import OutreachCreate, OutreachRead
from app.services.job_service import JobNotFoundError
from app.services.outreach_service import create_outreach, list_outreach_by_job

router = APIRouter(prefix="/outreach", tags=["outreach"])


@router.post("", response_model=OutreachRead, status_code=status.HTTP_201_CREATED)
def create_outreach_endpoint(payload: OutreachCreate, db: Session = Depends(get_db)) -> OutreachRead:
    try:
        return create_outreach(db, payload)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/job/{job_id}", response_model=list[OutreachRead])
def list_outreach_endpoint(job_id: str, db: Session = Depends(get_db)) -> list[OutreachRead]:
    try:
        return list_outreach_by_job(db, job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
