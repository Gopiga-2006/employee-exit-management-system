"""Password hashing, validation, and JWT helpers."""

import re
from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt

from app.core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET


def validate_password(password: str) -> str:
    """Validate the application's minimum password security policy."""
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError("Password must contain at least one special character")
    return password


def hash_password(password: str) -> str:
    """Hash a password before it is stored."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain password against its stored hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: int, role: str) -> str:
    """Create a signed token containing the user identity and role."""
    expires = datetime.now(UTC) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "exp": expires}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
