from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ExitRequest(Base):
    """Employee resignation request and its current workflow status."""

    __tablename__ = "exit_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    requested_last_working_date: Mapped[date] = mapped_column(Date, nullable=False)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    employee = relationship("User", back_populates="exit_requests")
    approvals = relationship("Approval", back_populates="exit_request", cascade="all, delete-orphan")
    clearance_tasks = relationship("ClearanceTask", back_populates="exit_request", cascade="all, delete-orphan")
