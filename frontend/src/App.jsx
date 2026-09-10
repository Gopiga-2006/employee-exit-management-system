import { useState } from "react";
import api from "./services/api";

export default function App() {
  const [reason, setReason] = useState("");
  const [lastWorkingDay, setLastWorkingDay] = useState("");
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState("");

  async function loadRequests() {
    const response = await api.get("/api/exit-requests/mine");
    setRequests(response.data);
  }

  async function submitRequest(event) {
    event.preventDefault();
    await api.post("/api/exit-requests", { reason, last_working_day: lastWorkingDay });
    setReason("");
    setLastWorkingDay("");
    setMessage("Exit request submitted successfully.");
    await loadRequests();
  }

  return (
    <main className="container py-5">
      <h1 className="mb-2">Employee Exit Management System</h1>
      <p className="text-secondary">Submit and track an employee exit request.</p>
      <form className="card p-4 mb-4" onSubmit={submitRequest}>
        <label className="form-label">Reason</label>
        <textarea className="form-control mb-3" value={reason} onChange={(e) => setReason(e.target.value)} required />
        <label className="form-label">Last Working Day</label>
        <input className="form-control mb-3" type="date" value={lastWorkingDay} onChange={(e) => setLastWorkingDay(e.target.value)} required />
        <button className="btn btn-primary" type="submit">Submit Exit Request</button>
      </form>
      {message && <div className="alert alert-success">{message}</div>}
      <button className="btn btn-outline-secondary mb-3" onClick={loadRequests}>View My Requests</button>
      <div className="list-group">
        {requests.map((request) => (
          <div className="list-group-item" key={request.id}>
            <strong>Request #{request.id}</strong>
            <div>{request.reason}</div>
            <small>Status: {request.status}</small>
          </div>
        ))}
      </div>
    </main>
  );
}
