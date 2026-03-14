import pandas as pd
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def align_forecasts(actuals: pd.DataFrame, forecasts: pd.DataFrame, horizon_hours: float) -> pd.DataFrame:
    """
    Aligns actual wind generation with the latest available forecast at a given horizon.
    - horizon_hours: 1.0 means we look for the forecast published 1 hour before target time.
    """
    if actuals.empty or forecasts.empty:
        return pd.DataFrame()

    results = []
    horizon_delta = timedelta(hours=horizon_hours)

    for _, actual_row in actuals.iterrows():
        target_time = actual_row['startTime']
        # The latest forecast that was published at or before (target_time - horizon)
        cutoff_time = target_time - horizon_delta
        
        # Filter forecasts for this target_time and valid publishTime
        possible = forecasts[
            (forecasts['startTime'] == target_time) & 
            (forecasts['publishTime'] <= cutoff_time)
        ]
        
        selected_forecast = None
        if not possible.empty:
            # Pick the absolutely latest available at that cutoff
            selected_forecast = possible.sort_values('publishTime', ascending=False).iloc[0]['generation']
        
        results.append({
            'timestamp': target_time,
            'actual': actual_row['generation'],
            'forecast': selected_forecast
        })

    merged = pd.DataFrame(results)
    
    # Linear Interpolation: If forecast (hourly) has gaps for 30m actuals
    # We only interpolate if we have some data
    if not merged.empty and merged['forecast'].count() > 0:
        merged.set_index('timestamp', inplace=True)
        merged['forecast'] = merged['forecast'].interpolate(method='linear')
        merged.reset_index(inplace=True)
    
    return merged[['timestamp', 'actual', 'forecast']]
