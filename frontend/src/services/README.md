# Frontend API Service

The frontend uses `src/services/api.js` as the single Axios client for communication with the FastAPI backend.

The client automatically uses `VITE_API_URL` when provided, falls back to the local FastAPI server, and adds the logged-in user's JWT as a Bearer token to protected requests.