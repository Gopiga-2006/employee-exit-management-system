"""Tests for authentication service functions."""

from app.services.auth_service import authenticate_user, create_user


def test_create_user_hashes_password(db_session):
    user = create_user(db_session, "Test User", "test@example.com", "secret123", "employee")

    assert user.id is not None
    assert user.password_hash != "secret123"
    assert authenticate_user(db_session, "test@example.com", "secret123") == user


def test_authenticate_user_rejects_invalid_password(db_session):
    create_user(db_session, "Test User", "test@example.com", "secret123", "employee")

    assert authenticate_user(db_session, "test@example.com", "wrongpass") is None
