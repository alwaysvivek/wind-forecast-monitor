import pandas as pd
from typing import Dict, Any, Optional
from src.schemas.forecast import ForecastSummary

def calculate_metrics(df: pd.DataFrame) -> ForecastSummary:
    """Calculates summary metrics from the aligned dataframe."""
    metrics = {}
    if df.empty:
        return ForecastSummary(msg="No data found for this range")
        
    valid_actuals = df['actual'].dropna()
    metrics['total_actual_gwh'] = float((valid_actuals.sum() * 0.5) / 1000) # MW * 0.5h = MWh, /1000 = GWh
    
    # MAE calculation where both exist
    comparison = df.dropna(subset=['actual', 'forecast'])
    if not comparison.empty:
        mae = (comparison['actual'] - comparison['forecast']).abs().mean()
        metrics['mae_mw'] = float(mae)
    else:
        metrics['mae_mw'] = None
        
    peak_row = df.loc[df['actual'].idxmax()] if not valid_actuals.empty else None
    metrics['peak_generation_mw'] = float(peak_row['actual']) if peak_row is not None else None
    metrics['peak_time'] = peak_row['timestamp'].isoformat() if peak_row is not None else None

    return ForecastSummary(**metrics)
