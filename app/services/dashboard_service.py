"""Dashboard aggregation functions for exit workflow data."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import ClearanceTask, ExitApproval, ExitInterview, ExitRequest


def get_exit_dashboard_poc(db: Session) -> dict[str, object]:
    """Build a small proof-of-concept view from existing exit workflow records."""
    status_rows = db.execute(
        select(ExitRequest.status, func.count(ExitRequest.id)).group_by(ExitRequest.status)
    ).all()
    status_counts = {status: count for status, count in status_rows}

    pending_clearances = db.scalar(
        select(func.count(ClearanceTask.id)).where(ClearanceTask.status == "Pending")
    ) or 0
    interviews_recorded = db.scalar(select(func.count(ExitInterview.id))) or 0
    approvals_recorded = db.scalar(select(func.count(ExitApproval.id))) or 0

    return {
        "status_counts": status_counts,
        "workflow_summary": {
            "pending_clearances": pending_clearances,
            "interviews_recorded": interviews_recorded,
            "approvals_recorded": approvals_recorded,
        },
    }
