from pydantic import BaseModel, Field


class OutreachGenerationRequest(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    role_title: str = Field(min_length=2, max_length=255)
    value_proposition: str = Field(min_length=10, max_length=2000)


class OutreachGenerationResponse(BaseModel):
    message: str
    provider: str
