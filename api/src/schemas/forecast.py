from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ForecastDataPoint(BaseModel):
    timestamp: datetime
    actual: Optional[float]
    forecast: Optional[float]

class ForecastSummary(BaseModel):
    total_actual_gwh: Optional[float] = None
    mae_mw: Optional[float] = None
    peak_generation_mw: Optional[float] = None
    peak_time: Optional[str] = None
    msg: Optional[str] = None

class ForecastResponse(BaseModel):
    data: List[ForecastDataPoint]
    summary: ForecastSummary
