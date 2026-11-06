import React from 'react';
import { AlertCircle, RefreshCw, Database } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ 
  message = "Loading historical Solcast data from FastAPI backend..." 
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 bg-surface-card border border-surface-border rounded-xl">
      <div className="flex items-center justify-center h-12 w-12 rounded-full bg-amber-500/10 border border-amber-500/20 text-solar-amber mb-4 animate-spin">
        <RefreshCw className="h-6 w-6" />
      </div>
      <p className="text-sm font-medium text-slate-200">{message}</p>
      <p className="text-xs text-slate-400 mt-1">Connecting to FastAPI analytics service (free tier cold starts may take ~30s)</p>
    </div>
  );
};

interface ErrorStateProps {
  error: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-6 bg-rose-500/5 border border-rose-500/20 rounded-xl text-center">
      <div className="flex items-center justify-center h-12 w-12 rounded-full bg-rose-500/10 text-rose-400 mb-3">
        <AlertCircle className="h-6 w-6" />
      </div>
      <h3 className="text-sm font-semibold text-rose-200">Failed to Load Backend Data</h3>
      <p className="text-xs text-slate-400 max-w-md mt-1 mb-4 leading-relaxed font-mono bg-surface p-2.5 rounded border border-surface-border">
        {error}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-card border border-surface-border hover:border-slate-500 text-xs font-medium text-slate-200 hover:text-white transition-colors"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          <span>Retry Request</span>
        </button>
      )}
    </div>
  );
};

interface EmptyStateProps {
  message?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  message = "No solar observations found for the selected query parameters."
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 bg-surface-card border border-surface-border rounded-xl text-center">
      <Database className="h-8 w-8 text-slate-500 mb-2" />
      <p className="text-xs text-slate-400">{message}</p>
    </div>
  );
};
