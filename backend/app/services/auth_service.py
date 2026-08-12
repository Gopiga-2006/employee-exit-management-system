from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


def register_user(db: Session, full_name: str, email: str, password: str, department_id: int | None) -> User:
    existing = db.scalar(select(User).where(User.email == email.lower()))
    if existing:
        raise ValueError("Email is already registered")
    user = User(full_name=full_name.strip(), email=email.lower(), password_hash=hash_password(password), role="employee", department_id=department_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if user and verify_password(password, user.password_hash):
        return user
    return None


def issue_token(user: User) -> str:
    return create_access_token(user.id, user.role)
