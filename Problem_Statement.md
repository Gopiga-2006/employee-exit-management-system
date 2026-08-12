# Problem Statement

## 1. Title
Employee Exit Management System

## 2. Domain
HRTech / Human Resources

## 3. Who is the user?
1. **Employee** — submits an exit request and checks its status.
2. **HR** — reviews exit requests, approves or rejects them, and tracks the exit process.
3. **Administrator** — manages the basic system data and can view exit records.

## 4. What problem are we solving?
Employee resignation and exit activities are often handled through emails, spreadsheets, and manual follow-ups. This makes it difficult for HR to know which requests are waiting for approval and which employees have completed the exit process. Employees also do not have one place to submit a request and check its status. The proposed system provides a simple web application for submitting, approving, and tracking employee exit requests.

## 5. Proposed Solution
The application will:
- Allow employees to create an account and log in.
- Allow employees to submit an exit request with resignation reason, requested last working date, and comments.
- Allow employees to view the status of their request.
- Allow HR users to view pending exit requests.
- Allow HR users to approve or reject an exit request with a comment.
- Show a simple HR dashboard with request counts.
- Keep approval records so the process can be audited later.

## 6. Core Entities / Database Tables
1. `users` — login and role information.
2. `departments` — department master data.
3. `exit_requests` — employee exit requests.
4. `approvals` — HR approval/rejection records.
5. `clearance_tasks` — simple exit clearance tasks connected to an approved request.

## 7. User Roles & Permissions
| Role | Permissions |
|---|---|
| Employee | Login, submit exit request, view own requests |
| HR | Login, view all requests, approve/reject requests, view dashboard |
| Admin | Login, view system records |

## 8. Success Criteria
- An employee can log in and submit an exit request in under 2 minutes.
- HR can see pending requests immediately after login.
- HR can approve or reject a request and the employee can see the updated status.
- The application stores the request and approval information in the database.

## 9. Out of Scope
- Payroll processing.
- Salary settlement calculation.
- Biometric attendance integration.
- Production email/SMS notifications in Review-I.
- AI-based attrition prediction; this can be considered for the later enhancement phase.

## 10. Chosen Track
**Python — FastAPI**
