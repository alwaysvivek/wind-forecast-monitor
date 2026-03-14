from fastapi import APIRouter, Query, HTTPException
from datetime import date, timedelta
import pandas as pd
import logging

from src.schemas.forecast import ForecastResponse, ForecastDataPoint
from src.services.elexon import fetch_actuals_sync, fetch_forecasts_sync
from src.services.alignment import align_forecasts
from src.services.metrics import calculate_metrics

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    horizon: float = Query(4.0, ge=0, le=48, description="Forecast horizon in hours")
):
    """
    Retrieves aligned actual vs forecast wind generation data.
    """
    logger.info(f"Request: {start_date} to {end_date}, horizon={horizon}")
    
    # Validation: STRICT January 2024 compliance
    JAN_START = date(2024, 1, 1)
    JAN_END = date(2024, 1, 31)
    
    if start_date < JAN_START or start_date > JAN_END or end_date < JAN_START or end_date > JAN_END:
        raise HTTPException(
            status_code=400, 
            detail="Strict Compliance Error: Only data for January 2024 is permitted."
        )

    try:
        # 1. Fetch data
        actuals_df = fetch_actuals_sync(start_date.isoformat(), end_date.isoformat())
        
        # Extend forecast window by 2 days back to ensure coverage for early target times
        f_start = (start_date - timedelta(days=2)).isoformat()
        forecasts_df = fetch_forecasts_sync(f_start, end_date.isoformat())
        
        if actuals_df.empty:
            return ForecastResponse(data=[], summary={"msg": "No actuals data found for this range"})

        # 2. Align & Interpolate
        aligned_df = align_forecasts(actuals_df, forecasts_df, horizon)
        
        # 3. Calculate metrics
        summary = calculate_metrics(aligned_df)

        # 4. Format response
        data_points = []
        for _, row in aligned_df.iterrows():
            data_points.append(
                ForecastDataPoint(
                    timestamp=row['timestamp'],
                    actual=row['actual'] if pd.notnull(row['actual']) else None,
                    forecast=row['forecast'] if pd.notnull(row['forecast']) else None
                )
            )
            
        return ForecastResponse(data=data_points, summary=summary)

    except Exception as e:
        logger.exception("Failed to process forecast request")
        raise HTTPException(status_code=500, detail=str(e))
