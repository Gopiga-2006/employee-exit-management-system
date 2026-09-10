"""Exit request service functions."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import ExitRequest


def create_exit_request(db: Session, employee_id: int, reason: str, last_working_day: date) -> ExitRequest:
    """Create a pending exit request for an employee."""
    request = ExitRequest(employee_id=employee_id, reason=reason, last_working_day=last_working_day)
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def list_employee_requests(db: Session, employee_id: int) -> list[ExitRequest]:
    """Return exit requests belonging to one employee."""
    return list(db.scalars(select(ExitRequest).where(ExitRequest.employee_id == employee_id).order_by(ExitRequest.id.desc())))
