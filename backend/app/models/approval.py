from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Approval(Base):
    """HR decision recorded against an employee exit request."""

    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(primary_key=True)
    exit_request_id: Mapped[int] = mapped_column(ForeignKey("exit_requests.id"), nullable=False)
    approver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[str] = mapped_column(String(20), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    exit_request = relationship("ExitRequest", back_populates="approvals")
