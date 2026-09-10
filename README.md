# Employee Exit Management System

Employee Exit Management System is a full-stack application for submitting, reviewing, approving, and tracking employee exit requests.

## Live Demo
Not available during the initial development stage.

## Video Demo
Not available during the initial development stage.

## Overview
The system gives employees a structured way to submit exit requests and view their progress. HR users can review requests, manage approvals, record exit interviews, and track clearance activities. The application uses a React frontend, FastAPI backend, and MySQL database.

## Architecture Diagram
See `docs/diagrams/system-architecture.md`.

## Tech Stack
| Layer | Technology |
| --- | --- |
| Frontend | React.js, JavaScript, Bootstrap, Axios |
| Backend | Python, FastAPI |
| Authentication | JWT, bcrypt |
| Data Access | SQLAlchemy |
| Database | MySQL 8 |
| Testing | Pytest |
| API Documentation | FastAPI Swagger |

## Features
### Employee
- Register and sign in
- Submit an exit request
- View own exit requests and statuses

### HR
- Review employee exit requests
- Approve or reject requests
- Manage exit interviews
- Manage clearance tasks
- Review audit records

## Screenshots
Screenshots will be added after the main frontend screens are completed.

## Getting Started
### Prerequisites
- Python 3.10 or later
- Node.js 18 or later
- MySQL 8

### Backend
```text
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```text
cd frontend
npm install
npm run dev
```

### Environment Variables
Copy `.env.example` to `.env` and provide the local database and application settings.

## Environment Variables
| Name | Description | Required |
| --- | --- | --- |
| DATABASE_URL | MySQL connection string | Yes |
| JWT_SECRET | Secret used to sign login tokens | Yes |
| JWT_EXPIRE_MINUTES | Token lifetime in minutes | Yes |

## API Documentation
When the backend is running locally, Swagger is available at `/docs`.

## Running Tests
```text
pytest
```

## Deployment
Deployment will be completed during the later deployment phase. The planned platforms are listed in `docs/technology-stack.md`.

## Folder Structure
```text
app/
  api/
  core/
  models/
  schemas/
  services/
tests/
docs/
frontend/
```

## Future Enhancements
- Email notifications for important exit-process events
- Employee exit reports and summaries
- Additional HR workflow integrations

## License
MIT

## Author / Contact
Project owner: Gopiga-2006
