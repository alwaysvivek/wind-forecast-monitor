import pandas as pd
from datetime import timedelta

def align_forecasts(actuals: pd.DataFrame, forecasts: pd.DataFrame, horizon_hours: float) -> pd.DataFrame:
    if actuals.empty or forecasts.empty:
        return pd.DataFrame()

    results = []
    horizon_delta = timedelta(hours=horizon_hours)

    for _, actual_row in actuals.iterrows():
        target_time = actual_row['startTime']
        cutoff_time = target_time - horizon_delta
        
        possible = forecasts[
            (forecasts['startTime'] == target_time) & 
            (forecasts['publishTime'] <= cutoff_time)
        ]
        
        selected_forecast = None
        if not possible.empty:
            selected_forecast = possible.sort_values('publishTime', ascending=False).iloc[0]['generation']
        
        results.append({
            'timestamp': target_time,
            'actual': actual_row['generation'],
            'forecast': selected_forecast
        })

    merged = pd.DataFrame(results)
    if not merged.empty and merged['forecast'].count() > 0:
        merged.set_index('timestamp', inplace=True)
        merged['forecast'] = merged['forecast'].interpolate(method='linear')
        merged.reset_index(inplace=True)
    
    return merged[['timestamp', 'actual', 'forecast']]
