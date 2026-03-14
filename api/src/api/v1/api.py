from fastapi import APIRouter
from src.api.v1.endpoints import forecast, system

api_router = APIRouter()
api_router.include_router(forecast.router, tags=["Monitoring"])
api_router.include_router(system.router, tags=["System"])
