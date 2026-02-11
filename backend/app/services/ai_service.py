from app.config import get_settings
from app.schemas.ai import OutreachGenerationRequest, OutreachGenerationResponse


def generate_outreach(payload: OutreachGenerationRequest) -> OutreachGenerationResponse:
    settings = get_settings()
    # Placeholder for provider integration. Keeps service abstraction clean.
    if settings.openai_api_key:
        message = (
            f"Dear hiring team at {payload.company_name}, I am writing to express strategic interest in the "
            f"{payload.role_title} opportunity. Over the past decade I have led transformation efforts that "
            f"drove measurable growth, built resilient teams, and delivered enterprise-scale operating rigor. "
            f"My value proposition centers on {payload.value_proposition}. I would welcome a discussion about "
            "how that experience can accelerate your priorities."
        )
        provider = "configured-provider"
    else:
        message = (
            f"Subject: Strategic Interest in {payload.role_title} at {payload.company_name}\n\n"
            f"Hello,\n\nI am reaching out to share my interest in the {payload.role_title} role at "
            f"{payload.company_name}. Across executive leadership roles, I have consistently delivered "
            f"business impact through disciplined strategy, cross-functional alignment, and operating excellence. "
            f"A core differentiator I bring is {payload.value_proposition}.\n\n"
            "I would value the opportunity to connect and discuss how my background aligns with your growth "
            "agenda and leadership needs. If helpful, I can share a concise overview of relevant results and "
            "a proposed 90-day value plan.\n\nBest regards,\n[Your Name]"
        )
        provider = "mock"
    return OutreachGenerationResponse(message=message, provider=provider)
