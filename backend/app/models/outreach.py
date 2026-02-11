import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OutreachChannel(str, enum.Enum):
    LINKEDIN = "LinkedIn"
    EMAIL = "Email"
    PHONE = "Phone"


class ResponseStatus(str, enum.Enum):
    NO_RESPONSE = "No Response"
    RESPONDED = "Responded"
    MEETING_SCHEDULED = "Meeting Scheduled"


class OutreachRecord(Base):
    __tablename__ = "outreach_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("job_opportunities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    contact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_designation: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[OutreachChannel] = mapped_column(Enum(OutreachChannel), nullable=False)
    outreach_date: Mapped[date] = mapped_column(Date, nullable=False)
    response_status: Mapped[ResponseStatus] = mapped_column(Enum(ResponseStatus), nullable=False)
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    job = relationship("JobOpportunity", back_populates="outreach_records")
