from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Any
import os
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wind Forecast Monitor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Elexon API
    ELEXON_API_BASE_URL: str = "https://data.elexon.co.uk/bmrs/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://wind-forecast-monitor-one.vercel.app"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            if isinstance(v, str):
                return json.loads(v)
            return v
        raise ValueError(v)
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ANALYSIS_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "analysis")
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(BASE_DIR), ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
