# Employee Exit Management System

Employee Exit Management System is a full-stack application for submitting, reviewing, approving, and tracking employee exit requests.

## Live Demo
- Frontend: https://employee-exit-management-system.vercel.app
- Backend: https://employee-exit-management-system-ez72.onrender.com

## Video Demo
To be added.

## Overview
The system gives employees a structured way to submit exit requests and view their progress. HR users can review requests, manage approvals, record exit interviews, and track clearance activities. The application uses a React frontend, FastAPI backend, and MySQL database.

## Architecture Diagram
![System Architecture](docs/diagrams/system-architecture.svg)

Detailed diagrams are available in `docs/diagrams/`, including the architecture, entity relationship, class, and module diagrams.

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
- View exit status and progress dashboard

## Screenshots
Screenshots of the main application screens can be added here.

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
The application is deployed with the React frontend hosted on Vercel, the FastAPI backend hosted on Render, and MySQL hosted on Aiven.

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
