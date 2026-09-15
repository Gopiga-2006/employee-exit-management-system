"""SQLAlchemy models for the exit workflow."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """Store an application user and their role."""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30), default="employee")
    exit_requests: Mapped[list["ExitRequest"]] = relationship(back_populates="employee")


class ExitRequest(Base):
    """Store an employee exit request."""
    __tablename__ = "exit_requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(Text)
    last_working_day: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="Pending")
    employee: Mapped[User] = relationship(back_populates="exit_requests")
    approvals: Mapped[list["ExitApproval"]] = relationship(back_populates="request")
    interview: Mapped["ExitInterview | None"] = relationship(back_populates="request", uselist=False)
    clearance_tasks: Mapped[list["ClearanceTask"]] = relationship(back_populates="request")


class ExitApproval(Base):
    """Store an HR decision for an exit request."""
    __tablename__ = "exit_approvals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("exit_requests.id"))
    approver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    decision: Mapped[str] = mapped_column(String(30))
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    request: Mapped[ExitRequest] = relationship(back_populates="approvals")


class ExitInterview(Base):
    """Store an exit interview for a request."""
    __tablename__ = "exit_interviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("exit_requests.id"), unique=True)
    interview_date: Mapped[date] = mapped_column(Date)
    feedback: Mapped[str] = mapped_column(Text)
    request: Mapped[ExitRequest] = relationship(back_populates="interview")


class ClearanceTask(Base):
    """Store one clearance activity for an exit request."""
    __tablename__ = "clearance_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("exit_requests.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30), default="Pending")
    request: Mapped[ExitRequest] = relationship(back_populates="clearance_tasks")


class AuditLog(Base):
    """Store an important action performed in the application."""
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100))
    entity: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
