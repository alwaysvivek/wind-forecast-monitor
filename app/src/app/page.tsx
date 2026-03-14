"use client";

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Wind, 
  Activity, 
  BarChart3, 
  AlertCircle, 
  ChevronRight,
  TrendingUp,
  Clock,
  Calendar
} from 'lucide-react';
import { ForecastChart } from '@/components/dashboard/ForecastChart';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { fetchForecastData } from '@/lib/api';
import { ForecastDataPoint, ForecastSummary } from '@/types';
import { format, subDays, startOfMonth, endOfMonth, parseISO } from 'date-fns';
import { debounce } from 'lodash';

export default function Dashboard() {
  const [data, setData] = useState<ForecastDataPoint[]>([]);
  const [summary, setSummary] = useState<ForecastSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // States for controls
  const [startDate, setStartDate] = useState("2024-01-01");
  const [endDate, setEndDate] = useState("2024-01-07");
  const [horizon, setHorizon] = useState(4);

  const loadData = useCallback(async (s: string, e: string, h: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchForecastData(s, e, h);
      setData(response.data);
      setSummary(response.summary);
    } catch (err: any) {
      if (err.response?.status === 400) {
        setError("Strict Compliance Error: Only January 2024 data is allowed.");
      } else {
        setError(err.message || "Failed to fetch data");
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounced load to handle slider changes smoothly
  const debouncedLoad = useCallback(
    debounce((s: string, e: string, h: number) => loadData(s, e, h), 300),
    [loadData]
  );

  useEffect(() => {
    debouncedLoad(startDate, endDate, horizon);
  }, [startDate, endDate, horizon, debouncedLoad]);

  return (
    <div className="min-h-screen bg-slate-bg py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Wind className="text-wind-emerald w-6 h-6 animate-pulse" />
              <h1 className="text-2xl font-bold text-text-primary tracking-tight">Wind Forecast Monitor</h1>
            </div>
            <p className="text-text-secondary">National Grid Wind Generation Accuracy Tracker (January 2024)</p>
          </div>
          
          <div className="flex flex-wrap items-center gap-4 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center gap-2">
              <Calendar size={16} className="text-text-secondary" />
              <input 
                type="date" 
                value={startDate}
                min="2024-01-01"
                max="2024-01-31"
                onChange={(e) => {
                  const val = e.target.value;
                  if (val >= "2024-01-01" && val <= "2024-01-31") {
                    setStartDate(val);
                  }
                }}
                className="text-sm border-none focus:ring-0 cursor-pointer text-text-primary font-medium"
              />
              <span className="text-slate-300">to</span>
              <input 
                type="date" 
                value={endDate}
                min="2024-01-01"
                max="2024-01-31"
                onChange={(e) => {
                  const val = e.target.value;
                  if (val >= "2024-01-01" && val <= "2024-01-31") {
                    setEndDate(val);
                  }
                }}
                className="text-sm border-none focus:ring-0 cursor-pointer text-text-primary font-medium"
              />
            </div>
            <div className="w-px h-6 bg-slate-200 hidden md:block" />
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Clock size={16} className="text-text-secondary" />
                <span className="text-sm font-medium text-text-secondary">Horizon:</span>
                <span className="text-sm font-bold text-energy-blue font-mono min-w-[3rem] text-center">
                  {horizon}h
                </span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="48" 
                value={horizon}
                onChange={(e) => setHorizon(parseInt(e.target.value))}
                className="w-24 md:w-32 accent-energy-blue h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard 
            title="Total Generation" 
            value={summary?.total_actual_gwh?.toFixed(2)} 
            unit="GWh"
            icon={TrendingUp}
            color="text-energy-blue"
            description="Total energy produced in period"
          />
          <MetricCard 
            title="Mean Absolute Error" 
            value={summary?.mae_mw?.toFixed(0)} 
            unit="MW"
            icon={Activity}
            color="text-amber-500"
            description="Average deviation from forecast"
          />
          <MetricCard 
            title="Peak Generation" 
            value={summary?.peak_generation_mw} 
            unit="MW"
            icon={BarChart3}
            color="text-wind-emerald"
            description={summary?.peak_time ? `At ${format(parseISO(summary.peak_time), "MMM d, HH:mm")}` : ""}
          />
          <MetricCard 
            title="Data Coverage" 
            value={data.length > 0 ? "100" : "0"} 
            unit="%"
            icon={AlertCircle}
            color="text-slate-500"
            description={`${data.length} measurements found`}
          />
        </div>

        {/* Chart Section */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 overflow-hidden">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-semibold text-text-primary">Actual vs Forecasted Generation</h2>
              <p className="text-sm text-text-secondary">Comparing real-time generation (Blue) with latest forecast (Green)</p>
            </div>
            {loading && (
              <div className="flex items-center gap-2 text-energy-blue animate-pulse">
                <div className="w-2 h-2 bg-current rounded-full"></div>
                <span className="text-xs font-semibold uppercase tracking-wider">Syncing...</span>
              </div>
            )}
          </div>
          
          {error ? (
            <div className="h-[400px] flex flex-col items-center justify-center text-slate-400">
              <AlertCircle size={48} className="mb-4 text-red-400" />
              <p className="text-balance text-center max-w-md">{error}</p>
              <button 
                onClick={() => loadData(startDate, endDate, horizon)}
                className="mt-4 px-4 py-2 bg-energy-blue text-white rounded-lg text-sm font-medium"
              >
                Retry Connection
              </button>
            </div>
          ) : data.length > 0 ? (
            <ForecastChart data={data} horizon={horizon} />
          ) : !loading ? (
            <div className="h-[400px] flex items-center justify-center text-slate-400">
              No data available for the selected range.
            </div>
          ) : (
             <div className="h-[400px] flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-slate-100 border-t-energy-blue rounded-full animate-spin"></div>
             </div>
          )}
        </div>
        
        {/* Footer info */}
        <footer className="mt-8 pt-8 border-t border-slate-200 text-center">
          <p className="text-xs text-text-secondary">
            Data sourced from <a href="https://bmrs.elexon.co.uk" target="_blank" className="underline font-medium">Elexon BMRS</a> API. 
            Forecasts are selected based on the latest available at least {horizon} hours before target time.
          </p>
        </footer>
      </div>
    </div>
  );
}
