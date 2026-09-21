# API Contract

## Health
- `GET /api/health`

## Authentication
- `POST /api/auth/signup/request-otp` — public employee registration step that sends a 6-digit OTP.
- `POST /api/auth/signup/verify-otp` — verifies the OTP and creates the employee account.
- `POST /api/auth/signup` — legacy-compatible endpoint that starts the same OTP registration flow.
- `POST /api/auth/login`
- `GET /api/auth/me` — authenticated profile endpoint.

## Exit Requests
- `POST /api/exit-requests`
- `GET /api/exit-requests/mine`
- `GET /api/exit-requests/all` for HR users

## Exit Approvals
- `POST /api/approvals/{request_id}` — HR/admin.
- `GET /api/approvals/{request_id}` — HR/admin.
- `PUT /api/approvals/{approval_id}` — HR/admin.

## Exit Interviews
- `POST /api/interviews/{request_id}` for HR users
- `GET /api/interviews/{request_id}` for HR users

## Clearance Tasks
- `POST /api/clearance-tasks/{request_id}` for HR users
- `GET /api/clearance-tasks/{request_id}` for HR users
- `PUT /api/clearance-tasks/{task_id}` — HR/admin.
- `DELETE /api/clearance-tasks/{task_id}` — HR/admin.

## HR Dashboard
- `GET /api/dashboard` — HR/admin.

FastAPI publishes the interactive API documentation at `/docs` when the backend is running.
