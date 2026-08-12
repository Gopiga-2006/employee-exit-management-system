from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ClearanceTask(Base):
    """Simple exit clearance item created after HR approval."""

    __tablename__ = "clearance_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    exit_request_id: Mapped[int] = mapped_column(ForeignKey("exit_requests.id"), nullable=False)
    task_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)

    exit_request = relationship("ExitRequest", back_populates="clearance_tasks")
