# Employee Exit Management System

A beginner-friendly full-stack HR application for submitting, approving, and tracking employee exit requests.

**Current milestone: Review-I (MVP)**

## Tech Stack
- Frontend: React.js, JavaScript, Bootstrap, Axios
- Backend: Python, FastAPI
- Database: MySQL 8 (SQLite fallback for simple local testing)
- ORM: SQLAlchemy
- Authentication: JWT + bcrypt
- API documentation: FastAPI Swagger/OpenAPI
- Version control: Git + GitHub

## Review-I Features
### Employee
- Register and login
- Submit an exit request
- View submitted requests and status

### HR
- Login
- View dashboard counts
- View employee exit requests
- Approve or reject requests

### System
- Employee, HR and Admin roles
- Password hashing
- Database-backed exit workflow
- Automatic Swagger API documentation
- Approval record and clearance-task models

## Project Structure
```text
backend/
  app/
    api/
    core/
    models/
    schemas/
    services/
  tests/
frontend/
  src/
docs/diagrams/
```

## Run the Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger will be available at `http://127.0.0.1:8000/docs`.

## Run the Frontend
```bash
cd frontend
npm install
npm run dev
```

Vite normally starts at `http://localhost:5173`.

## MySQL Configuration
Create a MySQL database and set these variables in `backend/.env`:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_exit
SECRET_KEY=change-this-development-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

For quick local learning, the backend defaults to SQLite if `DATABASE_URL` is not supplied.

## Demo HR Account
The seed script creates:

```text
Email: hr@example.com
Password: Hr@12345
```

Run `python seed.py` from the backend directory before the HR demo.

## API
- `GET /api/health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/exit-requests`
- `GET /api/v1/exit-requests/mine`
- `GET /api/v1/exit-requests`
- `PATCH /api/v1/exit-requests/{request_id}/decision`
- `GET /api/v1/exit-requests/dashboard`

## Review-I Documentation
See `Problem_Statement.md` and the files under `docs/` for the Review-I checklist, demo flow and diagrams.

## Author
GitHub: **Gopiga-2006**  
Email: **gopigar10hrsk@gmail.com**
