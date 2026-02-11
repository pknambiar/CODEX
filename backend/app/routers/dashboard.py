from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard import DashboardMetrics
from app.services.dashboard_service import get_metrics

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
def get_dashboard_metrics_endpoint(db: Session = Depends(get_db)) -> DashboardMetrics:
    return get_metrics(db)
