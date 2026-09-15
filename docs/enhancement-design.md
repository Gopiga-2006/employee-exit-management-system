# Enhancement Design

## Enhancement

Exit Clearance and Status Dashboard

## Purpose

Provide HR users with one dashboard for reviewing employee exit progress without changing the existing exit request workflow.

## User Access

The dashboard will be available to users with the `hr` or `admin` role. Employee users will continue to use the existing employee dashboard.

## Dashboard Sections

### Status Summary

Display the number of exit requests in each current status, including Pending, Approved, and Rejected.

### Pending Actions

Show exit requests that require HR attention, together with relevant approval, interview, or clearance information available from existing records.

### Recent Exit Requests

Display recently submitted exit requests with the request ID, employee, last working day, and current status.

### Exit Progress

For a selected exit request, show the available workflow stages:

1. Exit request submitted.
2. HR approval recorded.
3. Exit interview recorded.
4. Clearance tasks completed.
5. Exit request completed through the existing workflow.

## Backend Design

Add a dashboard service that reads the existing `ExitRequest`, `ExitApproval`, `ExitInterview`, and `ClearanceTask` records. No new database table is required for the dashboard.

Expose a protected endpoint under `/api/dashboard` for HR users. The response will follow the existing API structure:

```text
{
  "success": true,
  "data": {
    "status_counts": {},
    "pending_actions": [],
    "recent_requests": [],
    "exit_progress": []
  },
  "message": "Dashboard data retrieved"
}
```

The endpoint will use the existing JWT authentication and role restrictions.

## Frontend Design

Add a dashboard view to the existing HR interface. The view will use Axios to request dashboard data and Bootstrap cards, tables, and status indicators to present the results.

The existing HR request-processing workflow will remain available. The dashboard will provide a consolidated view rather than replacing those controls.

## Data Sources

| Dashboard information | Existing source |
| --- | --- |
| Status counts | `ExitRequest.status` |
| Recent requests | `ExitRequest` |
| Approval progress | `ExitApproval` |
| Interview progress | `ExitInterview` |
| Clearance progress | `ClearanceTask` |

## Implementation Scope

Week 7 will validate the backend data aggregation and dashboard response structure through a small proof of concept. Week 8 will implement the complete backend endpoint, React dashboard, automated tests, and live integration.

## Acceptance Conditions

- HR users can retrieve consolidated dashboard information.
- Employee users cannot access the HR dashboard endpoint.
- Dashboard data comes from the existing exit workflow records.
- Existing exit request, approval, interview, and clearance workflows continue to work.
- The dashboard can identify requests requiring HR attention.
