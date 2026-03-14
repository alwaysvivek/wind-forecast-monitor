import httpx
import pandas as pd
from cachetools import cached, TTLCache
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

# Cache for 1 hour
actuals_cache = TTLCache(maxsize=100, ttl=3600)
forecasts_cache = TTLCache(maxsize=100, ttl=3600)

@cached(actuals_cache)
def fetch_actuals_sync(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch ACTUALS (FUELHH) for WIND."""
    url = f"{settings.ELEXON_API_BASE_URL}/datasets/FUELHH/stream"
    params = {
        "settlementDateFrom": start_date,
        "settlementDateTo": end_date,
        "fuelType": "WIND"
    }
    
    logger.info(f"Fetching ACTUALS from {url} with {params}")
    try:
        response = httpx.get(url, params=params, timeout=60.0)
        response.raise_for_status()
        data = response.json()
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        df['startTime'] = pd.to_datetime(df['startTime'])
        df['generation'] = pd.to_numeric(df['generation'], errors='coerce')
        return df[['startTime', 'generation']].sort_values('startTime')
    except Exception as e:
        logger.error(f"Error fetching ACTUALS: {e}")
        return pd.DataFrame()

@cached(forecasts_cache)
def fetch_forecasts_sync(publish_start: str, publish_end: str) -> pd.DataFrame:
    """Fetch FORECASTS (WINDFOR) based on publishDateTime limits."""
    url = f"{settings.ELEXON_API_BASE_URL}/datasets/WINDFOR/stream"
    params = {
        "publishDateTimeFrom": f"{publish_start}T00:00:00Z",
        "publishDateTimeTo": f"{publish_end}T23:59:59Z"
    }
    
    logger.info(f"Fetching FORECASTS from {url} with {params}")
    try:
        response = httpx.get(url, params=params, timeout=60.0)
        response.raise_for_status()
        data = response.json()
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        if 'publishTime' not in df.columns:
            logger.error("'publishTime' missing from forecast data!")
            return pd.DataFrame()

        df['startTime'] = pd.to_datetime(df['startTime'])
        df['publishTime'] = pd.to_datetime(df['publishTime'])
        df['generation'] = pd.to_numeric(df['generation'], errors='coerce')
        return df[['startTime', 'publishTime', 'generation']]
    except Exception as e:
        logger.error(f"Error fetching FORECASTS: {e}")
        return pd.DataFrame()
