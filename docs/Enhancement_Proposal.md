# Enhancement Proposal

## Enhancement
Exit Clearance and Status Dashboard

## Problem
Exit information is distributed across approval, interview, and clearance workflow records. HR users need a consolidated view to understand current exit status, pending actions, and overall progress.

## Proposed Solution
Add an HR dashboard that aggregates existing exit workflow data and presents status counts, pending actions, recent exit requests, and individual exit progress in one view.

## Technical Approach
- Add a protected FastAPI dashboard endpoint under `/api/dashboard`.
- Aggregate existing `ExitRequest`, `ExitApproval`, `ExitInterview`, and `ClearanceTask` records.
- Restrict dashboard access to HR and administrator roles.
- Add the dashboard view to the existing React HR interface using Axios and Bootstrap.
- Reuse the existing database and authentication mechanisms without adding a new database table.

## Acceptance Criteria
- Authorized HR users can view consolidated exit status information.
- Pending approval, interview, and clearance actions are visible where applicable.
- Recent exit requests and workflow progress are displayed.
- Employee users cannot access the HR dashboard endpoint.
- Existing exit request and approval workflows continue to work.
- The enhancement is covered by automated tests and is available in the live application.
