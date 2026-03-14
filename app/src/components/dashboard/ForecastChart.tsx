"use client";

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  ComposedChart
} from 'recharts';
import { format, parseISO } from 'date-fns';
import { ForecastDataPoint } from '@/types';

interface ForecastChartProps {
  data: ForecastDataPoint[];
  horizon: number;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white/90 backdrop-blur-sm border border-slate-200 p-3 rounded-lg shadow-xl text-sm">
        <p className="font-semibold text-slate-800 mb-1">
          {format(parseISO(label), 'MMM d, HH:mm')}
        </p>
        {payload.map((entry: any, index: number) => (
          <div key={index} className="flex items-center gap-2" style={{ color: entry.color }}>
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></span>
            <span className="capitalize">{entry.name}:</span>
            <span className="font-mono font-medium">
              {entry.value.toLocaleString()} MW
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export const ForecastChart: React.FC<ForecastChartProps> = ({ data, horizon }) => {
  return (
    <div className="w-full h-[450px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(str) => format(parseISO(str), 'MM/dd')}
            minTickGap={60}
            stroke="#64748B"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="#64748B"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(val) => `${val / 1000}k`}
            label={{ value: 'Generation (MW)', angle: -90, position: 'insideLeft', style: { fill: '#64748B', fontSize: 12 } }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            verticalAlign="top" 
            height={36} 
            iconType="circle"
          />
          
          <Line
            name="Actual Generation"
            type="monotone"
            dataKey="actual"
            stroke="#2563EB"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6, strokeWidth: 0 }}
          />
          
          <Line
            name={`Forecast (H-${horizon})`}
            type="monotone"
            dataKey="forecast"
            stroke="#10B981"
            strokeWidth={2.5}
            strokeDasharray="5 5"
            dot={false}
            activeDot={{ r: 4, strokeWidth: 0 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
