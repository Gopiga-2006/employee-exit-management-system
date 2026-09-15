"""Dashboard aggregation functions for exit workflow data."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import ClearanceTask, ExitApproval, ExitInterview, ExitRequest


def get_exit_dashboard_poc(db: Session) -> dict[str, object]:
    """Build the consolidated exit dashboard from existing workflow records."""
    status_rows = db.execute(
        select(ExitRequest.status, func.count(ExitRequest.id)).group_by(ExitRequest.status)
    ).all()
    status_counts = {status: count for status, count in status_rows}

    pending_clearances = db.scalar(
        select(func.count(ClearanceTask.id)).where(ClearanceTask.status == "Pending")
    ) or 0
    interviews_recorded = db.scalar(select(func.count(ExitInterview.id))) or 0
    approvals_recorded = db.scalar(select(func.count(ExitApproval.id))) or 0

    requests = db.execute(
        select(ExitRequest).order_by(ExitRequest.id.desc())
    ).scalars().all()

    pending_actions = []
    recent_requests = []
    exit_progress = []

    for request in requests:
        approvals = request.approvals
        interview = request.interview
        clearance_tasks = request.clearance_tasks

        if request.status == "Pending":
            pending_actions.append(
                {
                    "request_id": request.id,
                    "action": "HR approval",
                    "status": "Pending",
                }
            )

        if not approvals:
            pending_actions.append(
                {
                    "request_id": request.id,
                    "action": "Approval",
                    "status": "Pending",
                }
            )

        if not interview:
            pending_actions.append(
                {
                    "request_id": request.id,
                    "action": "Exit interview",
                    "status": "Pending",
                }
            )

        pending_tasks = [
            task for task in clearance_tasks if task.status == "Pending"
        ]
        for task in pending_tasks:
            pending_actions.append(
                {
                    "request_id": request.id,
                    "action": task.task,
                    "status": "Pending",
                }
            )

        recent_requests.append(
            {
                "request_id": request.id,
                "employee": request.employee.name,
                "last_working_day": request.last_working_day.isoformat(),
                "status": request.status,
            }
        )

        clearance_completed = bool(clearance_tasks) and all(
            task.status != "Pending" for task in clearance_tasks
        )

        exit_progress.append(
            {
                "request_id": request.id,
                "employee": request.employee.name,
                "status": request.status,
                "submitted": True,
                "approval_recorded": bool(approvals),
                "interview_recorded": interview is not None,
                "clearance_completed": clearance_completed,
                "completed": request.status == "Completed",
            }
        )

    return {
        "status_counts": status_counts,
        "pending_actions": pending_actions,
        "recent_requests": recent_requests[:5],
        "exit_progress": exit_progress,
        "workflow_summary": {
            "pending_clearances": pending_clearances,
            "interviews_recorded": interviews_recorded,
            "approvals_recorded": approvals_recorded,
        },
    }
