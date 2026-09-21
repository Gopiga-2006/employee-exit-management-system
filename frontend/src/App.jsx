import { useState } from "react";
import api from "./services/api";

function getErrorMessage(err, fallback) {
  return err.response?.data?.detail || err.response?.data?.message || err.message || fallback;
}

function Login({ onLogin, onForgotPassword }) {
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
      <button type="button" className="btn btn-link mt-2" onClick={onForgotPassword}>Forgot password?</button>
      {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
    </form>
  );
}

function ForgotPassword({ onComplete }) {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function requestOtp(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/forgot-password/request-otp", {
        email,
        new_password: newPassword,
      });
      setOtpSent(true);
      setMessage("If the account exists, a password reset OTP has been sent.");
    } catch (err) {
      setError(getErrorMessage(err, "OTP could not be sent"));
    } finally {
      setLoading(false);
    }
  }

  async function resetPassword(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/forgot-password/verify-otp", {
        email,
        otp,
      });
      setMessage("Password reset successful. You can sign in now.");
      setTimeout(onComplete, 800);
    } catch (err) {
      setError(getErrorMessage(err, "Password reset failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card p-4 mx-auto auth-card" onSubmit={otpSent ? resetPassword : requestOtp}>
      <h2>Forgot Password</h2>
      {!otpSent ? (
        <>
          <input className="form-control mb-3" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <input className="form-control mb-2" type="password" placeholder="New password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required minLength={8} />
          <div className="small text-secondary mb-3">Password: minimum 8 characters, with uppercase, lowercase, number, and special character.</div>
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Sending OTP..." : "Send Reset OTP"}
          </button>
        </>
      ) : (
        <>
          <div className="alert alert-info">Enter the 6-digit OTP sent to your email.</div>
          <input className="form-control mb-3" inputMode="numeric" maxLength={6} placeholder="Enter OTP" value={otp} onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))} required />
          <button className="btn btn-primary" type="submit" disabled={loading || otp.length !== 6}>
            {loading ? "Resetting..." : "Verify OTP & Reset Password"}
          </button>
        </>
      )}
      {message && <div className="alert alert-success mt-3 mb-0">{message}</div>}
      {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
    </form>
  );
}

function Signup({ onSignup }) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function requestOtp(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/signup/request-otp", form);
      setOtpSent(true);
      setMessage("OTP sent. Enter the 6-digit OTP to complete registration.");
    } catch (err) {
      setError(getErrorMessage(err, "OTP could not be sent"));
    } finally {
      setLoading(false);
    }
  }

  async function verifyOtp(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/signup/verify-otp", { email: form.email, otp });
      setMessage("Account created. You can sign in now.");
      onSignup();
    } catch (err) {
      setError(getErrorMessage(err, "OTP verification failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card p-4 mx-auto auth-card" onSubmit={otpSent ? verifyOtp : requestOtp}>
      <h2>Register</h2>
      {!otpSent ? (
        <>
          <input className="form-control mb-3" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input className="form-control mb-3" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="form-control mb-2" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required minLength={8} />
          <div className="small text-secondary mb-3">Password: minimum 8 characters, with uppercase, lowercase, number, and special character.</div>
          <button className="btn btn-outline-primary" type="submit" disabled={loading}>
            {loading ? "Sending OTP..." : "Send OTP"}
          </button>
        </>
      ) : (
        <>
          <div className="alert alert-info">A 6-digit OTP was sent for {form.email}.</div>
          <input className="form-control mb-3" inputMode="numeric" maxLength={6} placeholder="Enter OTP" value={otp} onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))} required />
          <button className="btn btn-primary" type="submit" disabled={loading || otp.length !== 6}>
            {loading ? "Verifying..." : "Verify OTP & Create Account"}
          </button>
          <button type="button" className="btn btn-link mt-2" onClick={() => { setOtpSent(false); setOtp(""); }}>Change registration details</button>
        </>
      )}
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

function AdminDashboard() {
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "hr" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function createUser(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      const response = await api.post("/api/admin/users", form);
      setMessage(response.data.message);
      setForm({ name: "", email: "", password: "", role: "hr" });
    } catch (err) {
      setError(getErrorMessage(err, "User could not be created"));
    }
  }

  return (
    <section>
      <div className="card p-4 mx-auto" style={{ maxWidth: "650px" }}>
        <h2>Administration</h2>
        <p className="text-secondary">Create managed employee, HR or administrator accounts.</p>
        <form onSubmit={createUser}>
          <input className="form-control mb-3" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input className="form-control mb-3" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="form-control mb-2" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required minLength={8} />
          <div className="small text-secondary mb-3">Password: minimum 8 characters, with uppercase, lowercase, number, and special character.</div>
          <select className="form-select mb-3" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="hr">HR</option>
            <option value="employee">Employee</option>
            <option value="admin">Admin</option>
          </select>
          <button className="btn btn-primary" type="submit">Create Account</button>
        </form>
        {message && <div className="alert alert-success mt-3 mb-0">{message}</div>}
        {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
      </div>
    </section>
  );
}

function HrDashboard({ user }) {
  const [requests, setRequests] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [interviews, setInterviews] = useState({});
  const [clearanceTasks, setClearanceTasks] = useState({});
  const [interviewForms, setInterviewForms] = useState({});
  const [clearanceForms, setClearanceForms] = useState({});

  async function loadActivity(requestList) {
    const interviewResults = await Promise.all(requestList.map(async (request) => {
      try {
        const response = await api.get(`/api/interviews/${request.id}`);
        return [request.id, response.data.data];
      } catch (err) {
        return [request.id, null];
      }
    }));
    const taskResults = await Promise.all(requestList.map(async (request) => {
      try {
        const response = await api.get(`/api/clearance-tasks/${request.id}`);
        return [request.id, response.data.data];
      } catch (err) {
        return [request.id, []];
      }
    }));
    setInterviews(Object.fromEntries(interviewResults));
    setClearanceTasks(Object.fromEntries(taskResults));
  }

  async function loadDashboard() {
    setError("");
    try {
      const [requestResponse, dashboardResponse] = await Promise.all([
        api.get("/api/exit-requests/all"),
        api.get("/api/dashboard"),
      ]);
      const requestList = requestResponse.data.data;
      setRequests(requestList);
      setDashboard(dashboardResponse.data.data);
      await loadActivity(requestList);
    } catch (err) {
      setError(getErrorMessage(err, "Dashboard could not be loaded"));
    }
  }

  async function processRequest(id, decision) {
    try {
      await api.post(`/api/approvals/${id}`, { decision, remarks: "Processed by HR" });
      setMessage(`Request #${id} processed.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Request could not be processed"));
    }
  }

  const statusCounts = dashboard?.status_counts || {};
  const workflowSummary = dashboard?.workflow_summary || {};
  const pendingActions = dashboard?.pending_actions || [];
  const recentRequests = dashboard?.recent_requests || [];
  const exitProgress = dashboard?.exit_progress || [];

  async function createInterview(requestId) {
    const form = interviewForms[requestId] || {};
    if (!form.interview_date || !form.feedback) {
      setError("Enter the interview date and feedback.");
      return;
    }
    try {
      await api.post(`/api/interviews/${requestId}`, form);
      setMessage(`Exit interview recorded for request #${requestId}.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Interview could not be recorded"));
    }
  }

  async function updateInterview(requestId) {
    const interview = interviews[requestId];
    const form = interviewForms[requestId] || interview || {};
    try {
      await api.put(`/api/interviews/${requestId}`, {
        interview_date: form.interview_date,
        feedback: form.feedback,
      });
      setMessage(`Exit interview updated for request #${requestId}.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Interview could not be updated"));
    }
  }

  async function createClearanceTask(requestId) {
    const task = clearanceForms[requestId]?.task?.trim();
    if (!task) {
      setError("Enter a clearance task.");
      return;
    }
    try {
      await api.post(`/api/clearance-tasks/${requestId}`, {
        assigned_to: user.id,
        task,
      });
      setClearanceForms({ ...clearanceForms, [requestId]: { task: "" } });
      setMessage(`Clearance task created for request #${requestId}.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Clearance task could not be created"));
    }
  }

  async function updateClearanceTask(taskId, requestId, status) {
    try {
      await api.put(`/api/clearance-tasks/${taskId}`, { status });
      setMessage(`Clearance task updated for request #${requestId}.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Clearance task could not be updated"));
    }
  }

  async function deleteClearanceTask(taskId, requestId) {
    try {
      await api.delete(`/api/clearance-tasks/${taskId}`);
      setMessage(`Clearance task deleted for request #${requestId}.`);
      await loadDashboard();
    } catch (err) {
      setError(getErrorMessage(err, "Clearance task could not be deleted"));
    }
  }

  function updateInterviewForm(requestId, field, value) {
    setInterviewForms({
      ...interviewForms,
      [requestId]: { ...(interviewForms[requestId] || interviews[requestId] || {}), [field]: value },
    });
  }

  return (
    <section>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>HR Exit Dashboard</h2>
        <button className="btn btn-outline-secondary" onClick={loadDashboard}>Refresh Dashboard</button>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}
      <div className="row g-3 mb-4">
        <div className="col-md-4"><div className="card p-3 h-100"><div className="text-secondary">Pending</div><div className="display-6">{statusCounts.Pending || 0}</div></div></div>
        <div className="col-md-4"><div className="card p-3 h-100"><div className="text-secondary">Approved</div><div className="display-6">{statusCounts.Approved || 0}</div></div></div>
        <div className="col-md-4"><div className="card p-3 h-100"><div className="text-secondary">Rejected</div><div className="display-6">{statusCounts.Rejected || 0}</div></div></div>
      </div>
      <div className="row g-3 mb-4">
        <div className="col-md-4"><div className="card p-3"><strong>Pending clearances</strong><div>{workflowSummary.pending_clearances || 0}</div></div></div>
        <div className="col-md-4"><div className="card p-3"><strong>Interviews recorded</strong><div>{workflowSummary.interviews_recorded || 0}</div></div></div>
        <div className="col-md-4"><div className="card p-3"><strong>Approvals recorded</strong><div>{workflowSummary.approvals_recorded || 0}</div></div></div>
      </div>

      <div className="row g-4 mb-4">
        <div className="col-lg-6">
          <div className="card p-4 h-100">
            <h3>Pending Actions</h3>
            {pendingActions.length === 0 ? <p className="text-secondary mb-0">No pending actions.</p> : pendingActions.map((action, index) => (
              <div className="border-bottom py-2" key={`${action.request_id}-${action.action}-${index}`}>
                <strong>Request #{action.request_id}</strong>
                <div>{action.action}</div>
                <span className="badge text-bg-warning">{action.status}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="col-lg-6">
          <div className="card p-4 h-100">
            <h3>Recent Exit Requests</h3>
            {recentRequests.length === 0 ? <p className="text-secondary mb-0">No recent exit requests.</p> : recentRequests.map((request) => (
              <div className="border-bottom py-2" key={request.request_id}>
                <strong>Request #{request.request_id}</strong>
                <div>{request.employee}</div>
                <div>Last working day: {request.last_working_day}</div>
                <span className="badge text-bg-secondary">{request.status}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card p-4 mb-4">
        <h3>Exit Progress</h3>
        {exitProgress.length === 0 ? <p className="text-secondary mb-0">No exit progress to display.</p> : exitProgress.map((progress) => (
          <div className="border-bottom py-3" key={progress.request_id}>
            <div className="d-flex justify-content-between align-items-center mb-2">
              <strong>Request #{progress.request_id} — {progress.employee}</strong>
              <span className="badge text-bg-secondary">{progress.status}</span>
            </div>
            <div className="row g-2 small">
              <div className="col-md-2">Submitted: {progress.submitted ? "Yes" : "No"}</div>
              <div className="col-md-2">Approval: {progress.approval_recorded ? "Recorded" : "Pending"}</div>
              <div className="col-md-2">Interview: {progress.interview_recorded ? "Recorded" : "Pending"}</div>
              <div className="col-md-3">Clearance: {progress.clearance_completed ? "Completed" : "Pending"}</div>
              <div className="col-md-3">Exit completed: {progress.completed ? "Yes" : "No"}</div>
            </div>
          </div>
        ))}
      </div>

      <h3>Exit Requests</h3>
      {requests.map((request) => (
        <div className="card p-3 mb-3" key={request.id}>
          <strong>Request #{request.id}</strong>
          <div>{request.reason}</div>
          <div>Last working day: {request.last_working_day}</div>
          <div className="mt-2">Status: {request.status}</div>
          {request.status === "Pending" && <div className="mt-3"><button className="btn btn-success me-2" onClick={() => processRequest(request.id, "Approved")}>Approve</button><button className="btn btn-outline-danger" onClick={() => processRequest(request.id, "Rejected")}>Reject</button></div>}

          <div className="border-top mt-3 pt-3">
            <h5>Exit Interview</h5>
            {interviews[request.id] ? (
              <>
                <div className="small mb-2">Recorded date: {interviews[request.id].interview_date}</div>
                <textarea className="form-control mb-2" value={(interviewForms[request.id] || interviews[request.id]).feedback || ""} onChange={(e) => updateInterviewForm(request.id, "feedback", e.target.value)} />
                <input className="form-control mb-2" type="date" value={(interviewForms[request.id] || interviews[request.id]).interview_date || ""} onChange={(e) => updateInterviewForm(request.id, "interview_date", e.target.value)} />
                <button className="btn btn-outline-primary btn-sm" onClick={() => updateInterview(request.id)}>Update Interview</button>
              </>
            ) : (
              <>
                <input className="form-control mb-2" type="date" value={interviewForms[request.id]?.interview_date || ""} onChange={(e) => updateInterviewForm(request.id, "interview_date", e.target.value)} />
                <textarea className="form-control mb-2" placeholder="Interview feedback" value={interviewForms[request.id]?.feedback || ""} onChange={(e) => updateInterviewForm(request.id, "feedback", e.target.value)} />
                <button className="btn btn-outline-primary btn-sm" onClick={() => createInterview(request.id)}>Record Interview</button>
              </>
            )}
          </div>

          <div className="border-top mt-3 pt-3">
            <h5>Clearance Tasks</h5>
            {(clearanceTasks[request.id] || []).map((task) => (
              <div className="border rounded p-2 mb-2" key={task.id}>
                <div><strong>{task.task}</strong> <span className="badge text-bg-secondary">{task.status}</span></div>
                <div className="mt-2">
                  <select className="form-select form-select-sm d-inline-block w-auto me-2" value={task.status} onChange={(e) => updateClearanceTask(task.id, request.id, e.target.value)}>
                    <option>Pending</option>
                    <option>Completed</option>
                  </select>
                  <button className="btn btn-outline-danger btn-sm" onClick={() => deleteClearanceTask(task.id, request.id)}>Delete</button>
                </div>
              </div>
            ))}
            <div className="input-group mt-2">
              <input className="form-control" placeholder="New clearance task" value={clearanceForms[request.id]?.task || ""} onChange={(e) => setClearanceForms({ ...clearanceForms, [request.id]: { task: e.target.value } })} />
              <button className="btn btn-outline-success" onClick={() => createClearanceTask(request.id)}>Add Task</button>
            </div>
            <div className="small text-secondary mt-1">New tasks are assigned to the signed-in HR user.</div>
          </div>
        </div>
      ))}
    </section>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  const [mode, setMode] = useState("login");

  if (!user) {
    return <main className="container py-5"><h1 className="text-center mb-4">Employee Exit Management System</h1>{mode === "login" ? <Login onLogin={setUser} onForgotPassword={() => setMode("forgot")} /> : mode === "forgot" ? <ForgotPassword onComplete={() => setMode("login")} /> : <Signup onSignup={() => setMode("login")} />}<div className="text-center mt-3"><button className="btn btn-link" onClick={() => setMode(mode === "login" ? "signup" : "login")}>{mode === "login" ? "Create an account" : "Back to sign in"}</button></div></main>;
  }

  return <main className="container py-5"><div className="d-flex justify-content-between align-items-center mb-4"><div><h1>Employee Exit Management System</h1><div className="text-secondary">Signed in as {user.name} ({user.role})</div></div><button className="btn btn-outline-secondary" onClick={() => { localStorage.removeItem("access_token"); setUser(null); }}>Sign Out</button></div>{user.role === "employee" ? <EmployeeDashboard /> : user.role === "admin" ? <AdminDashboard /> : <HrDashboard user={user} />}</main>;
}
