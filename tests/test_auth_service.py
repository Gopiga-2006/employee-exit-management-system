"""Tests for authentication service functions."""

from app.core.security import validate_password
from app.services.auth_service import authenticate_user, create_user, verify_signup_otp


def test_password_policy_accepts_strong_password():
    assert validate_password("Employee@123") == "Employee@123"


def test_password_policy_rejects_weak_password():
    for password in ["secret12", "PASSWORD@1", "password@1", "Password@"]:
        try:
            validate_password(password)
        except ValueError:
            continue
        raise AssertionError(f"Expected password validation to fail: {password}")


def test_create_user_hashes_password(db_session):
    user = create_user(db_session, "Test User", "test@example.com", "Employee@123", "employee")

    assert user.id is not None
    assert user.password_hash != "Employee@123"
    assert authenticate_user(db_session, "test@example.com", "Employee@123") == user


def test_authenticate_user_rejects_invalid_password(db_session):
    create_user(db_session, "Test User", "test@example.com", "Employee@123", "employee")

    assert authenticate_user(db_session, "test@example.com", "Wrong@123") is None
