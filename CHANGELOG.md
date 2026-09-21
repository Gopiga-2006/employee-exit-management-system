# Changelog

## 2026-09-21
- Restricted public registration to employee accounts and kept privileged roles out of the signup flow.
- Added audit logging for exit requests, approvals, interviews, and clearance activities.
- Added activity service coverage and tests for the major exit workflow modules.
- Updated API and ER documentation for OTP registration and current endpoints.

## Week 1
- Added the finalized problem statement, project setup, and domain plan.

## Week 2
- Added system architecture, ER design, module design, API contract, backend structure, database models, authentication, and initial employee exit request flow.

## Week 3
- Added authenticated exit request processing, HR approvals, exit interview APIs, clearance task APIs, and frontend integration.

## Review-II
- Completed the core employee exit workflow, role-based access, automated tests, CI/CD pipeline, and cloud deployment.

## Review-III Enhancement
- Added the Exit Clearance and Status Dashboard for HR users.
- Added status aggregation, pending actions, recent exit requests, and exit progress views.
- Added automated dashboard service coverage and protected dashboard access.
- Integrated the enhancement into the live application.


## Security Enhancement
- Added strong password validation requiring at least 8 characters, uppercase, lowercase, number, and special character.
- Added registration OTP verification with expiry and attempt limits.
- Added configurable SMTP OTP delivery with console delivery available for local development.
