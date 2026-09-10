# Problem Statement

## 1. Title
Employee Exit Management System

## 2. Domain
Human Resources Management

## 3. Who is the user?
- Employee: submits an exit request and checks its progress.
- HR Executive: reviews exit requests and manages exit activities.
- HR Administrator: manages users, roles, and administrative access.

## 4. What problem are we solving?
Employee exit activities are often handled through emails, spreadsheets, and separate records. This makes it difficult for employees to know the current status of their exit request and for HR to track approvals, interviews, clearance activities, and completion. Important information can be missed when several teams handle the same exit process. The system will provide one place to submit, review, approve, and track employee exit requests.

## 5. Proposed Solution
The application will provide:
- Employee registration and login.
- Employee exit request submission and status tracking.
- HR review and approval of exit requests.
- Exit interview record management.
- Clearance task management.
- Audit records for important exit-process actions.
- Role-based access for employees and HR users.
- A REST API for communication between the frontend and backend.

## 6. Core Entities / Database Tables
1. Users
2. Exit Requests
3. Exit Approvals
4. Exit Interviews
5. Clearance Tasks
6. Audit Logs

## 7. User Roles & Permissions
- Employee: create an exit request, view their own requests, and view their exit status.
- HR Executive: view employee exit requests, approve or reject requests, manage interviews, and manage clearance tasks.
- HR Administrator: manage HR access and review administrative records.

## 8. Success Criteria
- An employee can submit an exit request and receive a recorded status.
- HR can review and process an exit request.
- HR can record an exit interview and clearance activities.
- Important actions are stored with their user and time information.
- Data is stored in related database tables and is available through the application interface.

## 9. Out of Scope
- Payroll processing.
- Recruitment management.
- Attendance management.
- Production deployment during the initial development stage.
- Mobile application development.

## 10. Chosen Track
Python (FastAPI)
