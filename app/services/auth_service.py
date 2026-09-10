"""Authentication service functions."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.entities import User


def create_user(db: Session, name: str, email: str, password: str, role: str) -> User:
    """Create and persist a user with a hashed password."""
    user = User(name=name, email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Return a matching user when the supplied credentials are valid."""
    user = db.scalar(select(User).where(User.email == email))
    if user and verify_password(password, user.password_hash):
        return user
    return None
