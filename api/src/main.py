from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from src.api.v1.api import api_router
from src.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
🚀 **Wind Forecast Monitor API** provides high-precision alignment of UK wind generation data.

### Features
* **Dynamic Alignment**: Match 30m actuals with 60m forecasts using linear interpolation.
* **Horizon Simulation**: View specific forecast snapshots from 1 to 48 hours in advance.
* **Strict Compliance**: Hard-gated to the January 2024 data window.
""",
        version=settings.VERSION,
        openapi_tags=[
            {
                "name": "Monitoring",
                "description": "Core wind forecast monitoring and alignment endpoints.",
            },
            {
                "name": "System",
                "description": "Health checks and system status.",
            },
        ],
        contact={
            "name": "Support",
            "url": "https://github.com/alwaysvivek",
        },
    )

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Mount analysis directory for report access
    if os.path.exists(settings.ANALYSIS_DIR):
        app.mount("/analysis", StaticFiles(directory=settings.ANALYSIS_DIR), name="analysis")

    # Include API Router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", include_in_schema=False)
    def root_redirect():
        return RedirectResponse(url=f"{settings.API_V1_STR}/health")

    return app

app = create_app()
