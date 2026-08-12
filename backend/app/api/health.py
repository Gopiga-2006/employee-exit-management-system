from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["System"])


@router.get("/health")
def health():
    return {"success": True, "data": {"status": "OK"}, "message": "Service is running"}
