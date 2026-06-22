import type { ReactNode } from "react";
import { Section, StatCard, Spark } from "@/components/wynthora";

const s = (n: number, len = 36) => Array.from({ length: len }, (_, i) => 50 + Math.sin(i / 3 + n) * 25 + Math.random() * 8);

export function ModulePage({ kicker, title, kpis, color, extras }: { kicker: string; title: string; color: string; kpis: { label: string; value: string; delta?: string }[]; extras?: ReactNode }) {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">{kicker}</p>
        <h1 className="font-display text-3xl font-bold">{title}</h1>
      </div>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {kpis.map((k, i) => <StatCard key={k.label} {...k} data={s(i + 1)} color={color} />)}
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        <Section title="Forecast 2025–2030" className="lg:col-span-2">
          <svg viewBox="0 0 600 220" className="w-full">
            <defs><linearGradient id={`mp-${title}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity="0.5" /><stop offset="100%" stopColor={color} stopOpacity="0" /></linearGradient></defs>
            {Array.from({ length: 5 }).map((_, i) => <line key={i} x1="0" y1={i * 50} x2="600" y2={i * 50} stroke="oklch(1 0 0 / 0.05)" />)}
            <path d="M0 160 Q 100 140 200 130 T 400 100 T 600 70" fill="none" stroke={color} strokeWidth="2.5" />
            <path d="M0 160 Q 100 110 200 95 T 400 60 T 600 30 L 600 110 Q 400 140 200 165 T 0 180 Z" fill={`url(#mp-${title})`} />
            <path d="M0 160 Q 100 175 200 185 T 400 200 T 600 195" fill="none" stroke={color} strokeWidth="1" strokeDasharray="4 4" opacity="0.5" />
          </svg>
        </Section>
        <Section title="Top drivers">
          <ul className="space-y-2 text-sm">
            {["Monetary policy", "Energy prices", "Geopolitical risk", "Climate events", "Tech productivity"].map((d, i) => (
              <li key={d} className="glass rounded-lg p-2.5">
                <div className="flex justify-between text-xs"><span>{d}</span><span className="font-mono text-muted-foreground">{(Math.random() * 2).toFixed(2)}σ</span></div>
                <div className="mt-1.5 h-1 rounded-full bg-muted overflow-hidden"><div className="h-full rounded-full" style={{ width: `${30 + i * 12}%`, background: color }} /></div>
              </li>
            ))}
          </ul>
        </Section>
      </div>
      {extras}
    </div>
  );
}
