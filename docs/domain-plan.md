# Domain Plan

## Objective
Provide a single workflow for employee exit requests from submission through HR processing and completion.

## Main Users
### Employee
- Creates an exit request.
- Provides a reason and planned last working day.
- Views the current request status.

### HR Executive
- Views submitted requests.
- Reviews request details.
- Records approval decisions.
- Records exit interviews.
- Assigns and updates clearance tasks.

### HR Administrator
- Maintains user access and administrative records.
- Reviews audit records.

## Main Workflow
1. Employee registers and signs in.
2. Employee submits an exit request.
3. HR reviews the request.
4. HR records an approval decision.
5. HR schedules or records the exit interview.
6. Clearance tasks are assigned and updated.
7. The request moves through its tracked status until completion.
8. Important actions are recorded in the audit log.

## Business Rules
- Every exit request belongs to one employee.
- An employee can view only their own requests.
- HR users can review employee requests.
- Only pending requests can be changed or removed by the employee.
- An approval belongs to one exit request and one HR user.
- An interview belongs to one exit request.
- Clearance tasks belong to an exit request and can be assigned to an HR user.
- Audit records store the user, action, and time of important changes.

## Initial Core API Areas
- Authentication
- Exit requests
- Exit approvals
- Exit interviews
- Clearance tasks
- Audit records

## Third-Party Integration Scope
The design leaves room for an email service to send exit-process notifications at a later stage.
