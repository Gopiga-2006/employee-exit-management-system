import os

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.department import Department
from app.models.user import User


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Department).count():
            db.add_all([Department(name="IT"), Department(name="HR"), Department(name="Finance")])
            db.commit()
        hr = db.query(User).filter(User.email == "hr@example.com").first()
        if not hr:
            hr_dept = db.query(Department).filter(Department.name == "HR").first()
            db.add(User(full_name="HR Manager", email="hr@example.com", password_hash=hash_password(os.environ.get("DEMO_HR_PASSWORD", "Hr@12345")), role="hr", department_id=hr_dept.id if hr_dept else None))
            db.commit()
            print("Created demo HR account: hr@example.com")
        else:
            print("Demo HR account already exists: hr@example.com / Hr@12345")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
