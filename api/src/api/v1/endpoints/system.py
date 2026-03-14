from fastapi import APIRouter, Request
import time
import os
import httpx
from src.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    """
    Production-grade Health Check.
    Verifies API connectivity and system uptime.
    """
    uptime_seconds = time.time() - request.app.state.start_time
    
    # Dependency Check: Ping Elexon with a valid (light) request
    elexon_status = "unknown"
    try:
        async with httpx.AsyncClient() as client:
            # We use a real (but tiny) request because BMRS returns 404 for empty queries
            elexon_url = f"{settings.ELEXON_API_BASE_URL}/datasets/FUELHH/stream"
            params = {
                "settlementDateFrom": "2024-01-01",
                "settlementDateTo": "2024-01-01",
                "fuelType": "WIND"
            }
            response = await client.get(elexon_url, params=params, timeout=5.0)
            elexon_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        elexon_status = "unreachable"

    return {
        "status": "ok" if elexon_status == "healthy" else "degraded",
        "version": settings.VERSION,
        "uptime_formatted": time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)),
        "dependencies": {
            "elexon_bmrs_api": elexon_status
        },
        "environment": "production" if os.getenv("RENDER") else "development"
    }
