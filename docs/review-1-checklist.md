# Review-I Checklist

## Required by Day 11

- [x] Problem statement finalized.
- [x] Architecture diagram v1.
- [x] ER diagram v1 with 5 tables.
- [x] Class/module diagram v1.
- [x] Modular backend structure.
- [x] README v1.
- [x] Login/signup API and UI.
- [x] JWT authentication.
- [x] Employee submits exit request.
- [x] Employee views request status.
- [x] HR views requests and dashboard counts.
- [x] HR approves/rejects request.
- [x] Approved requests create clearance tasks.
- [x] Automated test files included.

## Two Core End-to-End Flows

### Flow 1 — Employee Exit Request
Login/register → React form → FastAPI → SQLAlchemy → database → response → employee request list.

### Flow 2 — HR Approval
HR login → HR dashboard → FastAPI → database → approve/reject → approval record + status update → dashboard refresh.
