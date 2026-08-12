from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def create_hr():
    db = SessionLocal()
    try:
        user = User(full_name="HR Manager", email="hr@example.com", password_hash=hash_password("Hr@12345"), role="hr")
        db.add(user)
        db.commit()
    finally:
        db.close()


def test_employee_submit_and_hr_approve(client):
    employee = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test Employee", "email": "employee@example.com", "password": "Secret1"},
    ).json()["data"]
    employee_token = employee["access_token"]

    response = client.post(
        "/api/v1/exit-requests",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={"reason": "Personal reasons", "requested_last_working_date": "2099-12-31", "comments": "Please process my exit request."},
    )
    assert response.status_code == 201
    request_id = response.json()["data"]["id"]
    assert response.json()["data"]["status"] == "pending"

    create_hr()
    hr_token = client.post("/api/v1/auth/login", json={"email": "hr@example.com", "password": "Hr@12345"}).json()["data"]["access_token"]

    response = client.patch(
        f"/api/v1/exit-requests/{request_id}/decision",
        headers={"Authorization": f"Bearer {hr_token}"},
        json={"decision": "approved", "comment": "Approved by HR."},
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "approved"
