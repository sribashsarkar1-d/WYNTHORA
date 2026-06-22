import { createFileRoute } from "@tanstack/react-router";
import { Section, StatCard, Spark, Badge, Globe } from "@/components/wynthora";
import { AlertTriangle, Sparkles, TrendingUp } from "lucide-react";

export const Route = createFileRoute("/app/dashboard")({ component: Dashboard });

const s = (n: number) => Array.from({ length: 24 }, (_, i) => 50 + Math.sin(i / 2 + n) * 20 + Math.random() * 10);

function Dashboard() {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground">Sovereign Console · Live</p>
          <h1 className="font-display text-3xl font-bold">Global Situation Room</h1>
        </div>
        <div className="flex gap-2">
          <Badge tone="success">All systems nominal</Badge>
          <Badge tone="warning">3 active risk alerts</Badge>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Global GDP est." value="$108.4T" delta="+2.4%" data={s(1)} />
        <StatCard label="Geopolitical risk" value="6.8 / 10" delta="+0.3" data={s(2)} color="var(--color-purple)" />
        <StatCard label="Active sims" value="12,847" delta="+412" data={s(3)} color="var(--color-success)" />
        <StatCard label="Atlantic SST anomaly" value="+1.34°C" delta="+0.08" data={s(4)} color="var(--color-warning)" />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Section title="World Overview" className="lg:col-span-2">
          <div className="flex items-center justify-center py-4"><Globe size={320} /></div>
          <div className="grid grid-cols-4 gap-2 text-center text-xs">
            {[["NA", "Stable", "success"], ["EU", "Watch", "warning"], ["APAC", "Stable", "success"], ["MENA", "Critical", "danger"]].map(([r, s, t]) => (
              <div key={r} className="glass rounded-lg p-3"><div className="font-mono text-muted-foreground">{r}</div><div className="mt-1"><Badge tone={t as any}>{s}</Badge></div></div>
            ))}
          </div>
        </Section>

        <div className="space-y-4">
          <Section title="AI Insights" action={<Sparkles className="h-4 w-4 text-purple" />}>
            <ul className="space-y-3 text-sm">
              {[
                { t: "Brent crude likely to test $112 within 21 days (P=0.74)", c: "Macro Agent" },
                { t: "Taiwan strait tension index up 18% w/w — review supply chain B17", c: "Geo Agent" },
                { t: "EUR/USD ensemble diverging — increased volatility expected", c: "FX Agent" },
              ].map((i) => (
                <li key={i.t} className="glass rounded-lg border border-purple/20 p-3">
                  <div className="text-foreground">{i.t}</div>
                  <div className="mt-1 text-[10px] uppercase tracking-wider text-purple">{i.c}</div>
                </li>
              ))}
            </ul>
          </Section>
          <Section title="Risk Alerts" action={<AlertTriangle className="h-4 w-4 text-destructive" />}>
            <ul className="space-y-2 text-sm">
              {[
                ["Red Sea shipping disruption", "danger"],
                ["Argentina sovereign downgrade", "warning"],
                ["Pacific cyclone formation", "warning"],
              ].map(([t, tone]) => (
                <li key={t} className="flex items-center justify-between rounded-lg border border-border px-3 py-2">
                  <span>{t}</span><Badge tone={tone as any}>active</Badge>
                </li>
              ))}
            </ul>
          </Section>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Section title="Market Forecast 30d" action={<TrendingUp className="h-3 w-3 text-cyan" />}>
          <Spark data={s(10)} h={120} />
          <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
            <div><div className="text-muted-foreground">S&P 500</div><div className="text-success">+3.2%</div></div>
            <div><div className="text-muted-foreground">10Y UST</div><div className="text-warning">+12bp</div></div>
            <div><div className="text-muted-foreground">DXY</div><div className="text-destructive">-1.4%</div></div>
          </div>
        </Section>
        <Section title="Climate Indicators">
          <Spark data={s(20)} h={120} color="var(--color-warning)" />
          <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
            <div><div className="text-muted-foreground">CO₂ ppm</div><div>424.7</div></div>
            <div><div className="text-muted-foreground">Arctic ice</div><div className="text-destructive">-8.2%</div></div>
            <div><div className="text-muted-foreground">El Niño</div><div>Moderate</div></div>
          </div>
        </Section>
        <Section title="Political Stability">
          <Spark data={s(30)} h={120} color="var(--color-purple)" />
          <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
            <div><div className="text-muted-foreground">Elections Q</div><div>23</div></div>
            <div><div className="text-muted-foreground">Conflicts</div><div className="text-destructive">14</div></div>
            <div><div className="text-muted-foreground">Coup risk</div><div className="text-warning">3</div></div>
          </div>
        </Section>
      </div>
    </div>
  );
}
