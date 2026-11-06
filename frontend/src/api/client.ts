import type {
  HealthResponse,
  CitiesResponse,
  SummaryResponse,
  TimeseriesResponse,
  AggregateMetricsResponse,
  CityWiseMetricsResponse,
  FeatureImportanceResponse,
  PredictionsResponse,
  AnomaliesResponse
} from './types';

// Use environment variable if explicitly configured; otherwise default to relative path ''
// Strips trailing slashes to prevent malformed double-slash URLs (e.g., https://api.onrender.com//api/health)
const rawBaseUrl = import.meta.env.VITE_API_BASE_URL;
const API_BASE_URL = 
  rawBaseUrl && typeof rawBaseUrl === 'string' && rawBaseUrl.trim() !== ''
    ? rawBaseUrl.trim().replace(/\/+$/, '')
    : '';

async function handleResponse<T>(res: Response): Promise<T> {
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('text/html')) {
    throw new Error(
      `Received HTML instead of JSON from ${res.url}. ` +
      `If deployed on Vercel, ensure VITE_API_BASE_URL is set to your Render backend URL in Vercel Project Settings, then redeploy.`
    );
  }

  if (!res.ok) {
    let errorDetail = `HTTP ${res.status}: ${res.statusText}`;
    try {
      const errorJson = await res.json();
      if (errorJson && errorJson.detail) {
        errorDetail = typeof errorJson.detail === 'string' 
          ? errorJson.detail 
          : JSON.stringify(errorJson.detail);
      }
    } catch {
      // Body is not JSON, use status text
    }
    throw new Error(errorDetail);
  }
  return res.json() as Promise<T>;
}

export const api = {
  /**
   * Check backend health and dataset presence
   */
  async getHealth(): Promise<HealthResponse> {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    return handleResponse<HealthResponse>(res);
  },

  /**
   * Fetch all registered cities with geographical metadata
   */
  async getCities(): Promise<CitiesResponse> {
    const res = await fetch(`${API_BASE_URL}/api/analytics/cities`);
    return handleResponse<CitiesResponse>(res);
  },

  /**
   * Fetch historical summary statistics for a city
   */
  async getSummary(location: string): Promise<SummaryResponse> {
    const params = new URLSearchParams({ location });
    const res = await fetch(`${API_BASE_URL}/api/analytics/summary?${params.toString()}`);
    return handleResponse<SummaryResponse>(res);
  },

  /**
   * Fetch 15-minute time-series observations normalized to IST for charting
   */
  async getTimeseries(location: string, startDate: string, endDate: string): Promise<TimeseriesResponse> {
    const params = new URLSearchParams({
      location,
      start_date: startDate,
      end_date: endDate,
    });
    const res = await fetch(`${API_BASE_URL}/api/analytics/timeseries?${params.toString()}`);
    return handleResponse<TimeseriesResponse>(res);
  },

  /**
   * Fetch aggregate ML holdout evaluation metrics (Mean baseline, Persistence, RF)
   */
  async getMlMetrics(): Promise<AggregateMetricsResponse> {
    const res = await fetch(`${API_BASE_URL}/api/ml/metrics`);
    return handleResponse<AggregateMetricsResponse>(res);
  },

  /**
   * Fetch location-specific holdout performance (RF vs Persistence)
   */
  async getCityMetrics(): Promise<CityWiseMetricsResponse> {
    const res = await fetch(`${API_BASE_URL}/api/ml/city-metrics`);
    return handleResponse<CityWiseMetricsResponse>(res);
  },

  /**
   * Fetch Gini feature importance ranking
   */
  async getFeatureImportance(): Promise<FeatureImportanceResponse> {
    const res = await fetch(`${API_BASE_URL}/api/ml/feature-importance`);
    return handleResponse<FeatureImportanceResponse>(res);
  },

  /**
   * Fetch offline test holdout predictions (actual vs predicted GHI and persistence)
   */
  async getPredictions(location?: string, date?: string, limit: number = 500): Promise<PredictionsResponse> {
    const params = new URLSearchParams();
    if (location) params.append('location', location);
    if (date) params.append('date', date);
    if (limit) params.append('limit', limit.toString());
    const res = await fetch(`${API_BASE_URL}/api/ml/predictions?${params.toString()}`);
    return handleResponse<PredictionsResponse>(res);
  },

  /**
   * Fetch 99th-percentile residual anomalies
   */
  async getAnomalies(location?: string, severity?: string, limit: number = 250): Promise<AnomaliesResponse> {
    const params = new URLSearchParams();
    if (location) params.append('location', location);
    if (severity) params.append('severity', severity);
    if (limit) params.append('limit', limit.toString());
    const res = await fetch(`${API_BASE_URL}/api/ml/anomalies?${params.toString()}`);
    return handleResponse<AnomaliesResponse>(res);
  },
};
