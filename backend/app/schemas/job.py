from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ApplicationStatus, JobSource


class JobBase(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    role_title: str = Field(min_length=2, max_length=255)
    location: str = Field(min_length=2, max_length=255)
    compensation_band: str | None = Field(default=None, max_length=255)
    source: JobSource
    application_status: ApplicationStatus = ApplicationStatus.IDENTIFIED
    notes: str | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=2, max_length=255)
    role_title: str | None = Field(default=None, min_length=2, max_length=255)
    location: str | None = Field(default=None, min_length=2, max_length=255)
    compensation_band: str | None = Field(default=None, max_length=255)
    source: JobSource | None = None
    application_status: ApplicationStatus | None = None
    notes: str | None = None


class JobRead(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    date_added: datetime
    last_updated: datetime
