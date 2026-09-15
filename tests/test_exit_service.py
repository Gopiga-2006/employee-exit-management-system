"""Tests for exit request service functions."""

from datetime import date

from app.services.auth_service import create_user
from app.services.exit_service import create_exit_request, list_employee_requests


def test_create_exit_request_sets_pending_status(db_session):
    employee = create_user(db_session, "Employee One", "employee1@example.com", "secret123", "employee")

    request = create_exit_request(
        db_session,
        employee.id,
        "Career change",
        date(2026, 10, 31),
    )

    assert request.id is not None
    assert request.employee_id == employee.id
    assert request.reason == "Career change"
    assert request.last_working_day == date(2026, 10, 31)
    assert request.status == "Pending"


def test_list_employee_requests_returns_only_employee_requests(db_session):
    employee_one = create_user(db_session, "Employee One", "employee1@example.com", "secret123", "employee")
    employee_two = create_user(db_session, "Employee Two", "employee2@example.com", "secret123", "employee")

    first_request = create_exit_request(
        db_session,
        employee_one.id,
        "Relocation",
        date(2026, 10, 15),
    )
    create_exit_request(
        db_session,
        employee_two.id,
        "Higher studies",
        date(2026, 11, 15),
    )
    second_request = create_exit_request(
        db_session,
        employee_one.id,
        "Personal reasons",
        date(2026, 12, 15),
    )

    requests = list_employee_requests(db_session, employee_one.id)

    assert [request.id for request in requests] == [second_request.id, first_request.id]


def test_list_employee_requests_returns_empty_for_employee_without_requests(db_session):
    employee = create_user(db_session, "Employee One", "employee1@example.com", "secret123", "employee")

    assert list_employee_requests(db_session, employee.id) == []
