"""Audit logging service functions."""

from sqlalchemy.orm import Session

from app.models.entities import AuditLog


def record_audit(db: Session, user_id: int, action: str, entity: str) -> AuditLog:
    """Record an important application action."""
    log = AuditLog(user_id=user_id, action=action, entity=entity)
    db.add(log)
    return log
