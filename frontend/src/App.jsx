import { useState } from "react";
import api from "./services/api";

function getErrorMessage(err, fallback) {
  return err.response?.data?.detail || err.response?.data?.message || err.message || fallback;
}

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const response = await api.post("/api/auth/login", { email, password });
      const result = response.data.data;
      localStorage.setItem("access_token", result.access_token);
      onLogin(result.user);
    } catch (err) {
      setError(getErrorMessage(err, "Login failed"));
    }
  }

  return (
    <form className="card p-4 mx-auto auth-card" onSubmit={submit}>
      <h2>Sign In</h2>
      <input className="form-control mb-3" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input className="form-control mb-3" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      <button className="btn btn-primary" type="submit">Sign In</button>
      {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
    </form>
  );
}

function Signup({ onSignup }) {
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "employee" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/signup", form);
      setMessage("Account created. You can sign in now.");
      onSignup();
    } catch (err) {
      setError(getErrorMessage(err, "Account could not be created"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card p-4 mx-auto auth-card" onSubmit={submit}>
      <h2>Register</h2>
      <input className="form-control mb-3" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
      <input className="form-control mb-3" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
      <input className="form-control mb-3" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
      <select className="form-select mb-3" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
        <option value="employee">Employee</option>
        <option value="hr">HR Executive</option>
        <option value="admin">HR Administrator</option>
      </select>
      <button className="btn btn-outline-primary" type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Account"}
      </button>
      {message && <div className="alert alert-success mt-3 mb-0">{message}</div>}
      {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
    </form>
  );
}

function EmployeeDashboard() {
  const [reason, setReason] = useState("");
  const [lastWorkingDay, setLastWorkingDay] = useState("");
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState("");

  async function loadRequests() {
    const response = await api.get("/api/exit-requests/mine");
    setRequests(response.data.data);
  }

  async function submit(event) {
    event.preventDefault();
    await api.post("/api/exit-requests", { reason, last_working_day: lastWorkingDay });
    setReason("");
    setLastWorkingDay("");
    setMessage("Exit request submitted.");
    await loadRequests();
  }

  return (
    <section>
      <form className="card p-4 mb-4" onSubmit={submit}>
        <h2>Submit Exit Request</h2>
        <textarea className="form-control mb-3" placeholder="Reason" value={reason} onChange={(e) => setReason(e.target.value)} required />
        <input className="form-control mb-3" type="date" value={lastWorkingDay} onChange={(e) => setLastWorkingDay(e.target.value)} required />
        <button className="btn btn-primary" type="submit">Submit Request</button>
      </form>
      {message && <div className="alert alert-success">{message}</div>}
      <button className="btn btn-outline-secondary mb-3" onClick={loadRequests}>Refresh My Requests</button>
      {requests.map((request) => <div className="card p-3 mb-2" key={request.id}><strong>Request #{request.id}</strong><div>{request.reason}</div><span>Status: {request.status}</span></div>)}
    </section>
  );
}

function HrDashboard() {
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState("");

  async function loadRequests() {
    const response = await api.get("/api/exit-requests/all");
    setRequests(response.data.data);
  }

  async function processRequest(id, decision) {
    await api.post(`/api/approvals/${id}`, { decision, remarks: "Processed by HR" });
    setMessage(`Request #${id} processed.`);
    await loadRequests();
  }

  return (
    <section>
      <button className="btn btn-outline-secondary mb-3" onClick={loadRequests}>Refresh Exit Requests</button>
      {message && <div className="alert alert-success">{message}</div>}
      {requests.map((request) => (
        <div className="card p-3 mb-3" key={request.id}>
          <strong>Request #{request.id}</strong>
          <div>{request.reason}</div>
          <div>Last working day: {request.last_working_day}</div>
          <div className="mt-2">Status: {request.status}</div>
          {request.status === "Pending" && <div className="mt-3"><button className="btn btn-success me-2" onClick={() => processRequest(request.id, "Approved")}>Approve</button><button className="btn btn-outline-danger" onClick={() => processRequest(request.id, "Rejected")}>Reject</button></div>}
        </div>
      ))}
    </section>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  const [mode, setMode] = useState("login");

  if (!user) {
    return <main className="container py-5"><h1 className="text-center mb-4">Employee Exit Management System</h1>{mode === "login" ? <Login onLogin={setUser} /> : <Signup onSignup={() => setMode("login")} />}<div className="text-center mt-3"><button className="btn btn-link" onClick={() => setMode(mode === "login" ? "signup" : "login")}>{mode === "login" ? "Create an account" : "Back to sign in"}</button></div></main>;
  }

  return <main className="container py-5"><div className="d-flex justify-content-between align-items-center mb-4"><div><h1>Employee Exit Management System</h1><div className="text-secondary">Signed in as {user.name} ({user.role})</div></div><button className="btn btn-outline-secondary" onClick={() => { localStorage.removeItem("access_token"); setUser(null); }}>Sign Out</button></div>{user.role === "employee" ? <EmployeeDashboard /> : <HrDashboard />}</main>;
}
