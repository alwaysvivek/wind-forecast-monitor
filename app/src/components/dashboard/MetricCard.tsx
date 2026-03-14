"use client";

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number | undefined;
  unit?: string;
  icon: LucideIcon;
  description?: string;
  color?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({ 
  title, 
  value, 
  unit, 
  icon: Icon, 
  description,
  color = "text-energy-blue" 
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm transition-all hover:shadow-md">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-text-secondary">{title}</p>
          <div className="mt-2 flex items-baseline">
            <h3 className="text-2xl font-bold text-text-primary font-mono">
              {value !== undefined ? value.toLocaleString() : '---'}
            </h3>
            {unit && <span className="ml-1 text-xs font-semibold text-text-secondary uppercase">{unit}</span>}
          </div>
          {description && <p className="mt-1 text-xs text-text-secondary">{description}</p>}
        </div>
        <div className={`p-2 rounded-lg bg-slate-50 ${color}`}>
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
};
