import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class JobSource(str, enum.Enum):
    LINKEDIN = "LinkedIn"
    RECRUITER = "Recruiter"
    REFERRAL = "Referral"
    SEARCH_FIRM = "Search Firm"


class ApplicationStatus(str, enum.Enum):
    IDENTIFIED = "Identified"
    APPLIED = "Applied"
    RECRUITER_CONTACTED = "Recruiter Contacted"
    INTERVIEW_STAGE = "Interview Stage"
    OFFER = "Offer"
    CLOSED = "Closed"


class JobOpportunity(Base):
    __tablename__ = "job_opportunities"
    __table_args__ = (UniqueConstraint("company_name", "role_title", name="uq_company_role"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    compensation_band: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[JobSource] = mapped_column(Enum(JobSource), nullable=False)
    application_status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.IDENTIFIED, nullable=False, index=True
    )
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    outreach_records = relationship(
        "OutreachRecord", back_populates="job", cascade="all, delete-orphan", passive_deletes=True
    )
