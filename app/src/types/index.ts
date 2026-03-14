export interface ForecastDataPoint {
  timestamp: string;
  actual: number | null;
  forecast: number | null;
}

export interface ForecastSummary {
  total_actual_gwh?: number;
  mae_mw?: number;
  peak_generation_mw?: number;
  peak_time?: string;
  msg?: string;
}

export interface ForecastResponse {
  data: ForecastDataPoint[];
  summary: ForecastSummary;
}
