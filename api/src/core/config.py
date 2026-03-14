from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wind Forecast Monitor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Elexon API
    ELEXON_API_BASE_URL: str = "https://data.elexon.co.uk/bmrs/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
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
