from fastapi import APIRouter

from app.schemas.ai import OutreachGenerationRequest, OutreachGenerationResponse
from app.services.ai_service import generate_outreach

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-outreach", response_model=OutreachGenerationResponse)
def generate_outreach_endpoint(payload: OutreachGenerationRequest) -> OutreachGenerationResponse:
    return generate_outreach(payload)
