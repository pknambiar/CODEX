from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models import OutreachChannel, ResponseStatus


class OutreachBase(BaseModel):
    contact_name: str = Field(min_length=2, max_length=255)
    contact_designation: str = Field(min_length=2, max_length=255)
    channel: OutreachChannel
    outreach_date: date
    response_status: ResponseStatus
    follow_up_date: date | None = None
    notes: str | None = None


class OutreachCreate(OutreachBase):
    job_id: str


class OutreachRead(OutreachBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    job_id: str
