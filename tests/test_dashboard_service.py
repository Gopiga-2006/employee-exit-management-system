"""Tests for dashboard aggregation functions."""

from datetime import date

from app.models.entities import ClearanceTask, ExitApproval, ExitInterview
from app.services.auth_service import create_user
from app.services.dashboard_service import get_exit_dashboard_poc
from app.services.exit_service import create_exit_request


def test_dashboard_summary_aggregates_exit_workflow_records(db_session):
    employee = create_user(db_session, "Employee One", "employee1@example.com", "secret123", "employee")
    hr = create_user(db_session, "HR User", "hr1@example.com", "secret123", "hr")

    pending_request = create_exit_request(
        db_session,
        employee.id,
        "Career change",
        date(2026, 10, 31),
    )
    approved_request = create_exit_request(
        db_session,
        employee.id,
        "Relocation",
        date(2026, 11, 30),
    )
    approved_request.status = "Approved"
    db_session.add(ExitApproval(request_id=approved_request.id, approver_id=hr.id, decision="Approved"))
    db_session.add(
        ExitInterview(
            request_id=approved_request.id,
            interview_date=date(2026, 10, 20),
            feedback="Completed",
        )
    )
    db_session.add(
        ClearanceTask(
            request_id=pending_request.id,
            assigned_to=hr.id,
            task="Asset return",
            status="Pending",
        )
    )
    db_session.commit()

    result = get_exit_dashboard_poc(db_session)

    assert result["status_counts"] == {"Pending": 1, "Approved": 1}
    assert result["workflow_summary"] == {
        "pending_clearances": 1,
        "interviews_recorded": 1,
        "approvals_recorded": 1,
    }


def test_dashboard_summary_is_empty_without_exit_records(db_session):
    result = get_exit_dashboard_poc(db_session)

    assert result["status_counts"] == {}
    assert result["workflow_summary"] == {
        "pending_clearances": 0,
        "interviews_recorded": 0,
        "approvals_recorded": 0,
    }
