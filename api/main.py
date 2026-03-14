from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, date
import logging
import pandas as pd
import os

from data_service import fetch_actuals_sync, fetch_forecasts_sync
from forecast_logic import align_forecasts

app = FastAPI(title="Wind Forecast Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/forecast")
def get_forecast(
    start_date: date,
    end_date: date,
    horizon: float = 4.0
):
    actuals_df = fetch_actuals_sync(start_date.isoformat(), end_date.isoformat())
    forecasts_df = fetch_forecasts_sync(start_date.isoformat(), end_date.isoformat())
    aligned_df = align_forecasts(actuals_df, forecasts_df, horizon)
    return {"data": aligned_df.to_dict(orient="records"), "summary": {}}
