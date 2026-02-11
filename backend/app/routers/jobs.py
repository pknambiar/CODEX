from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job_service import (
    DuplicateJobError,
    JobNotFoundError,
    create_job,
    delete_job,
    get_job_or_404,
    list_jobs,
    update_job,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job_endpoint(payload: JobCreate, db: Session = Depends(get_db)) -> JobRead:
    try:
        return create_job(db, payload)
    except DuplicateJobError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[JobRead])
def list_jobs_endpoint(
    status_filter: str | None = Query(default=None, alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
) -> list[JobRead]:
    return list_jobs(db, status=status_filter, skip=skip, limit=limit, sort_order=sort_order)


@router.get("/{job_id}", response_model=JobRead)
def get_job_endpoint(job_id: str, db: Session = Depends(get_db)) -> JobRead:
    try:
        return get_job_or_404(db, job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/{job_id}", response_model=JobRead)
def update_job_endpoint(job_id: str, payload: JobUpdate, db: Session = Depends(get_db)) -> JobRead:
    try:
        return update_job(db, job_id, payload)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DuplicateJobError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_endpoint(job_id: str, db: Session = Depends(get_db)) -> None:
    try:
        delete_job(db, job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
