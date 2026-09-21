"""Authentication service functions."""

from datetime import UTC, datetime, timedelta
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.email import send_otp_email
from app.core.security import hash_password, verify_password
from app.models.entities import OtpVerification, User

OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 10
MAX_OTP_ATTEMPTS = 5


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


def request_signup_otp(
    db: Session,
    name: str,
    email: str,
    password: str,
    role: str,
) -> None:
    """Create a time-limited registration OTP and deliver it."""
    db.query(OtpVerification).filter(OtpVerification.email == email).delete(
        synchronize_session=False
    )
    otp = f"{secrets.randbelow(10**OTP_LENGTH):0{OTP_LENGTH}d}"
    pending = OtpVerification(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        otp_hash=hash_password(otp),
        expires_at=datetime.now(UTC).replace(tzinfo=None)
        + timedelta(minutes=OTP_EXPIRE_MINUTES),
    )
    db.add(pending)
    db.commit()
    send_otp_email(email, otp)

def request_password_reset_otp(db: Session, email: str, new_password: str) -> None:
    """Create a time-limited password reset OTP for an existing user."""
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return
    db.query(OtpVerification).filter(OtpVerification.email == email).delete(
        synchronize_session=False
    )
    otp = f"{secrets.randbelow(10**OTP_LENGTH):0{OTP_LENGTH}d}"
    pending = OtpVerification(
        name=user.name,
        email=email,
        password_hash=hash_password(new_password),
        role="password_reset",
        otp_hash=hash_password(otp),
        expires_at=datetime.now(UTC).replace(tzinfo=None)
        + timedelta(minutes=OTP_EXPIRE_MINUTES),
    )
    db.add(pending)
    db.commit()
    send_otp_email(
        email,
        otp,
        "Employee Exit Management System - Password Reset OTP",
    )


def verify_password_reset_otp(db: Session, email: str, otp: str) -> bool:
    """Verify a password reset OTP and update the user's password."""
    pending = db.scalar(
        select(OtpVerification)
        .where(
            OtpVerification.email == email,
            OtpVerification.role == "password_reset",
        )
        .order_by(OtpVerification.id.desc())
    )
    if not pending:
        return False

    now = datetime.now(UTC).replace(tzinfo=None)
    if pending.expires_at < now or pending.attempts >= MAX_OTP_ATTEMPTS:
        db.delete(pending)
        db.commit()
        return False

    pending.attempts += 1
    if not verify_password(otp, pending.otp_hash):
        db.commit()
        return False

    user = db.scalar(select(User).where(User.email == email))
    if not user:
        db.delete(pending)
        db.commit()
        return False
    user.password_hash = pending.password_hash
    db.delete(pending)
    db.commit()
    return True



def verify_signup_otp(db: Session, email: str, otp: str) -> User | None:
    """Verify a registration OTP and create the pending user."""
    pending = db.scalar(
        select(OtpVerification)
        .where(OtpVerification.email == email)
        .order_by(OtpVerification.id.desc())
    )
    if not pending or pending.role != "employee":
        return None

    now = datetime.now(UTC).replace(tzinfo=None)
    if pending.expires_at < now or pending.attempts >= MAX_OTP_ATTEMPTS:
        db.delete(pending)
        db.commit()
        return None

    pending.attempts += 1
    if not verify_password(otp, pending.otp_hash):
        db.commit()
        return None

    user = User(
        name=pending.name,
        email=pending.email,
        password_hash=pending.password_hash,
        role=pending.role,
    )
    db.add(user)
    db.delete(pending)
    db.commit()
    db.refresh(user)
    return user
