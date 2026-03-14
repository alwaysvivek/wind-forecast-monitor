import axios from 'axios';
import { ForecastResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('--- API CONFIGURATION ---');
console.log('Connecting to:', API_BASE_URL);
console.log('Mode:', process.env.NODE_ENV);
console.log('-------------------------');

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60s timeout for Render free tier cold starts
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchForecastData = async (
  startDate: string,
  endDate: string,
  horizon: number
): Promise<ForecastResponse> => {
  try {
    const response = await apiClient.get<ForecastResponse>('/api/v1/forecast', {
      params: {
        start_date: startDate,
        end_date: endDate,
        horizon: horizon,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching forecast data:', error);
    throw error;
  }
};
