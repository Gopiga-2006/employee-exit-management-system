# API Contract

## Health
- `GET /api/health`
- Returns the service status.

## Authentication
- `POST /api/auth/signup`
- `POST /api/auth/login`

## Exit Requests
- `POST /api/exit-requests`
- `GET /api/exit-requests/mine`
- `GET /api/exit-requests/all` for HR users

## Exit Approvals
- `POST /api/approvals/{request_id}` for HR users

FastAPI publishes the interactive API documentation at `/docs` when the backend is running.
