import { Activity, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

interface HealthMetrics {
  score: number;
  coverage: number;
  quality: number;
  completeness: number;
}

export function HealthDashboard({ metrics }: { metrics?: HealthMetrics }) {
  const defaultMetrics = metrics || {
    score: 85,
    coverage: 78,
    quality: 92,
    completeness: 88
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-secondary';
    if (score >= 60) return 'text-[var(--accent-color)]';
    return 'text-destructive';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-secondary/10';
    if (score >= 60) return 'bg-[var(--accent-color)]/10';
    return 'bg-destructive/10';
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-2 rounded-lg bg-primary/10 text-primary">
          <Activity className="w-4 h-4" />
        </div>
        <div>
          <h3 className="text-sm font-semibold">Documentation Health</h3>
          <p className="text-xs text-muted-foreground">Quality metrics & insights</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          label="Overall Score"
          value={defaultMetrics.score}
          icon={<TrendingUp className="w-4 h-4" />}
        />
        <MetricCard
          label="Coverage"
          value={defaultMetrics.coverage}
          icon={<CheckCircle className="w-4 h-4" />}
        />
        <MetricCard
          label="Quality"
          value={defaultMetrics.quality}
          icon={<AlertCircle className="w-4 h-4" />}
        />
        <MetricCard
          label="Completeness"
          value={defaultMetrics.completeness}
          icon={<Activity className="w-4 h-4" />}
        />
      </div>

      <div className="mt-4 p-3 rounded-lg bg-muted/30">
        <div className="flex items-start gap-2">
          <div className={`p-1.5 rounded-lg ${getScoreBg(defaultMetrics.score)} ${getScoreColor(defaultMetrics.score)}`}>
            {defaultMetrics.score >= 80 ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
          </div>
          <div className="flex-1">
            <p className="text-xs font-medium mb-0.5">
              {defaultMetrics.score >= 80 ? 'Excellent Documentation!' : 'Good Documentation'}
            </p>
            <p className="text-xs text-muted-foreground">
              {defaultMetrics.score >= 80
                ? 'Your documentation meets high quality standards.'
                : 'Consider improving coverage for better documentation health.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, icon }: { label: string; value: number; icon: React.ReactNode }) {
  const getColor = (val: number) => {
    if (val >= 80) return 'text-secondary';
    if (val >= 60) return 'text-[var(--accent-color)]';
    return 'text-destructive';
  };

  return (
    <div className="p-3 rounded-lg border border-border bg-card">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs text-muted-foreground">{label}</span>
        <div className="text-muted-foreground">{icon}</div>
      </div>
      <div className={`text-xl font-bold ${getColor(value)}`}>
        {value}%
      </div>
    </div>
  );
}
