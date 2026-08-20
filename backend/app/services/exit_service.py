from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.models.clearance_task import ClearanceTask
from app.models.exit_request import ExitRequest
from app.models.user import User


def create_exit_request(
    db: Session,
    employee: User,
    reason: str,
    requested_last_working_date: date,
    comments: str | None,
) -> ExitRequest:
    cleaned_reason = reason.strip()
    cleaned_comments = comments.strip() if comments else None

    if len(cleaned_reason) < 5:
        raise ValueError("Reason must contain at least 5 characters")
    if requested_last_working_date <= date.today():
        raise ValueError("Last working date must be in the future")

    existing = db.scalar(
        select(ExitRequest).where(
            ExitRequest.employee_id == employee.id,
            ExitRequest.status == "pending",
        )
    )
    if existing:
        raise ValueError("You already have a pending exit request")

    request = ExitRequest(
        employee_id=employee.id,
        reason=cleaned_reason,
        requested_last_working_date=requested_last_working_date,
        comments=cleaned_comments,
        status="pending",
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def approve_or_reject(
    db: Session,
    exit_request: ExitRequest,
    approver: User,
    decision: str,
    comment: str | None,
) -> ExitRequest:
    if exit_request.status != "pending":
        raise ValueError("Only pending requests can be reviewed")
    if decision not in {"approved", "rejected"}:
        raise ValueError("Decision must be approved or rejected")

    exit_request.status = decision
    db.add(
        Approval(
            exit_request_id=exit_request.id,
            approver_id=approver.id,
            decision=decision,
            comment=comment.strip() if comment else None,
        )
    )

    if decision == "approved":
        for task_name in ["IT assets", "HR documents", "Finance clearance"]:
            db.add(ClearanceTask(exit_request_id=exit_request.id, task_name=task_name))

    db.commit()
    db.refresh(exit_request)
    return exit_request


def to_response(item: ExitRequest) -> dict:
    return {
        "id": item.id,
        "employee_id": item.employee_id,
        "employee_name": item.employee.full_name,
        "reason": item.reason,
        "requested_last_working_date": item.requested_last_working_date,
        "comments": item.comments,
        "status": item.status,
        "created_at": item.created_at,
    }


def dashboard_counts(db: Session) -> dict[str, int]:
    rows = db.execute(
        select(ExitRequest.status, func.count(ExitRequest.id)).group_by(
            ExitRequest.status
        )
    ).all()
    counts = {"pending": 0, "approved": 0, "rejected": 0}
    for status_name, count in rows:
        counts[status_name] = count
    return counts
