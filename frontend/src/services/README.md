# Frontend API Service

The frontend uses `src/services/api.js` as the single Axios client for communication with the FastAPI backend.

The client automatically:

- Uses `VITE_API_URL` when provided.
- Falls back to the local FastAPI server at `http://127.0.0.1:8000`.
- Adds the logged-in user's JWT as a Bearer token to protected requests.

This keeps frontend-to-backend communication in one place and makes the application easier to configure for later cloud deployment.