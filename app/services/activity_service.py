"""Exit workflow activity service functions."""

from datetime import date

from sqlalchemy.orm import Session

from app.models.entities import ClearanceTask, ExitApproval, ExitInterview, ExitRequest
from app.services.audit_service import record_audit


def create_approval(db: Session, request_id: int, approver_id: int, decision: str, remarks: str | None) -> ExitApproval:
    """Create an approval decision and update the related request."""
    request = db.get(ExitRequest, request_id)
    if request is None:
        raise ValueError("Exit request not found")
    approval = ExitApproval(request_id=request_id, approver_id=approver_id, decision=decision, remarks=remarks)
    request.status = decision
    db.add(approval)
    record_audit(db, approver_id, f"Exit request {decision.lower()}", "exit_requests")
    db.commit()
    db.refresh(approval)
    return approval


def update_approval(db: Session, approval: ExitApproval, decision: str, remarks: str | None, user_id: int) -> ExitApproval:
    """Update an approval decision and the related request status."""
    approval.decision = decision
    approval.remarks = remarks
    request = db.get(ExitRequest, approval.request_id)
    if request:
        request.status = decision
    record_audit(db, user_id, f"Approval updated to {decision.lower()}", "exit_approvals")
    db.commit()
    db.refresh(approval)
    return approval


def create_interview(db: Session, request_id: int, interview_date: date, feedback: str, user_id: int) -> ExitInterview:
    """Create an exit interview record."""
    interview = ExitInterview(request_id=request_id, interview_date=interview_date, feedback=feedback)
    db.add(interview)
    record_audit(db, user_id, "Exit interview recorded", "exit_interviews")
    db.commit()
    db.refresh(interview)
    return interview


def update_interview(db: Session, interview: ExitInterview, interview_date: date, feedback: str, user_id: int) -> ExitInterview:
    """Update an exit interview record."""
    interview.interview_date = interview_date
    interview.feedback = feedback
    record_audit(db, user_id, "Exit interview updated", "exit_interviews")
    db.commit()
    db.refresh(interview)
    return interview


def create_clearance_task(db: Session, request_id: int, assigned_to: int, task: str, user_id: int) -> ClearanceTask:
    """Create a clearance task."""
    clearance = ClearanceTask(request_id=request_id, assigned_to=assigned_to, task=task)
    db.add(clearance)
    record_audit(db, user_id, "Clearance task created", "clearance_tasks")
    db.commit()
    db.refresh(clearance)
    return clearance


def update_clearance_task(db: Session, task: ClearanceTask, status: str, user_id: int) -> ClearanceTask:
    """Update a clearance task status."""
    task.status = status
    record_audit(db, user_id, "Clearance task updated", "clearance_tasks")
    db.commit()
    db.refresh(task)
    return task


def delete_clearance_task(db: Session, task: ClearanceTask, user_id: int) -> None:
    """Delete a clearance task and record the action."""
    record_audit(db, user_id, "Clearance task deleted", "clearance_tasks")
    db.delete(task)
    db.commit()
