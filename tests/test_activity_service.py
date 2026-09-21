"""Tests for exit workflow activity service functions."""

from datetime import date

from app.models.entities import AuditLog, ClearanceTask, ExitApproval, ExitInterview
from app.services.activity_service import (
    create_approval,
    create_clearance_task,
    create_interview,
    delete_clearance_task,
    update_clearance_task,
    update_interview,
)
from app.services.auth_service import create_user
from app.services.exit_service import create_exit_request


def test_approval_service_updates_request_and_audits(db_session):
    employee = create_user(db_session, "Employee", "employee@example.com", "Employee@123", "employee")
    hr = create_user(db_session, "HR", "hr@example.com", "Employee@123", "hr")
    request = create_exit_request(db_session, employee.id, "Career change", date(2026, 10, 31))

    approval = create_approval(db_session, request.id, hr.id, "Approved", "Approved by HR")

    assert approval.decision == "Approved"
    assert db_session.get(type(request), request.id).status == "Approved"
    assert db_session.query(ExitApproval).count() == 1
    assert db_session.query(AuditLog).count() == 2


def test_interview_service_creates_and_updates_record(db_session):
    employee = create_user(db_session, "Employee", "employee@example.com", "Employee@123", "employee")
    hr = create_user(db_session, "HR", "hr@example.com", "Employee@123", "hr")
    request = create_exit_request(db_session, employee.id, "Relocation", date(2026, 11, 30))

    interview = create_interview(db_session, request.id, date(2026, 10, 20), "Completed", hr.id)
    updated = update_interview(db_session, interview, date(2026, 10, 21), "Updated", hr.id)

    assert updated.feedback == "Updated"
    assert db_session.query(ExitInterview).count() == 1


def test_clearance_service_crud(db_session):
    employee = create_user(db_session, "Employee", "employee@example.com", "Employee@123", "employee")
    hr = create_user(db_session, "HR", "hr@example.com", "Employee@123", "hr")
    request = create_exit_request(db_session, employee.id, "Higher studies", date(2026, 12, 15))

    task = create_clearance_task(db_session, request.id, hr.id, "Asset return", hr.id)
    updated = update_clearance_task(db_session, task, "Completed", hr.id)

    assert updated.status == "Completed"
    assert db_session.query(ClearanceTask).count() == 1

    delete_clearance_task(db_session, updated, hr.id)
    assert db_session.query(ClearanceTask).count() == 0
