import httpx
import pandas as pd
from cachetools import cached, TTLCache

actuals_cache = TTLCache(maxsize=100, ttl=3600)
forecasts_cache = TTLCache(maxsize=100, ttl=3600)

@cached(actuals_cache)
def fetch_actuals_sync(start_date: str, end_date: str) -> pd.DataFrame:
    url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH/stream"
    params = {"settlementDateFrom": start_date, "settlementDateTo": end_date, "fuelType": "WIND"}
    response = httpx.get(url, params=params)
    df = pd.DataFrame(response.json())
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['generation'] = pd.to_numeric(df['generation'], errors='coerce')
    return df[['startTime', 'generation']].sort_values('startTime')

@cached(forecasts_cache)
def fetch_forecasts_sync(publish_start: str, publish_end: str) -> pd.DataFrame:
    url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR/stream"
    params = {"publishDateTimeFrom": f"{publish_start}T00:00:00Z", "publishDateTimeTo": f"{publish_end}T23:59:59Z"}
    response = httpx.get(url, params=params)
    df = pd.DataFrame(response.json())
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['publishTime'] = pd.to_datetime(df['publishTime'])
    df['generation'] = pd.to_numeric(df['generation'], errors='coerce')
    return df[['startTime', 'publishTime', 'generation']]
