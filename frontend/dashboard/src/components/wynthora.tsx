import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";

export function Globe({ size = 420 }: { size?: number }) {
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <div className="absolute inset-0 rounded-full" style={{ background: "radial-gradient(circle at 30% 30%, oklch(0.78 0.18 220 / 0.5), transparent 60%)", filter: "blur(40px)" }} />
      <svg viewBox="0 0 400 400" className="relative h-full w-full animate-[spin_60s_linear_infinite]">
        <defs>
          <radialGradient id="earth" cx="35%" cy="35%">
            <stop offset="0%" stopColor="oklch(0.45 0.18 220)" />
            <stop offset="60%" stopColor="oklch(0.22 0.10 250)" />
            <stop offset="100%" stopColor="oklch(0.10 0.05 250)" />
          </radialGradient>
          <linearGradient id="atm" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="oklch(0.78 0.18 220)" stopOpacity="0.6" />
            <stop offset="100%" stopColor="oklch(0.55 0.25 295)" stopOpacity="0.2" />
          </linearGradient>
        </defs>
        <circle cx="200" cy="200" r="195" fill="none" stroke="url(#atm)" strokeWidth="2" />
        <circle cx="200" cy="200" r="180" fill="url(#earth)" />
        {Array.from({ length: 12 }).map((_, i) => (
          <ellipse key={i} cx="200" cy="200" rx={180} ry={180 - i * 15} fill="none" stroke="oklch(0.78 0.18 220 / 0.15)" strokeWidth="0.5" />
        ))}
        {Array.from({ length: 9 }).map((_, i) => (
          <line key={i} x1={200 + Math.cos((i / 9) * Math.PI) * 180} y1={200 + Math.sin((i / 9) * Math.PI) * 180}
            x2={200 - Math.cos((i / 9) * Math.PI) * 180} y2={200 - Math.sin((i / 9) * Math.PI) * 180}
            stroke="oklch(0.78 0.18 220 / 0.15)" strokeWidth="0.5" />
        ))}
        {[[120, 140, 28], [260, 130, 22], [180, 220, 35], [290, 250, 18], [100, 240, 20], [220, 100, 14]].map(([x, y, r], i) => (
          <circle key={i} cx={x} cy={y} r={r} fill="oklch(0.72 0.18 155 / 0.5)" />
        ))}
        {[[80, 180], [320, 200], [200, 80], [200, 320], [150, 280], [280, 150]].map(([x, y], i) => (
          <g key={i}>
            <circle cx={x} cy={y} r="3" fill="oklch(0.82 0.18 215)" />
            <circle cx={x} cy={y} r="8" fill="none" stroke="oklch(0.82 0.18 215)" strokeWidth="1" opacity="0.5">
              <animate attributeName="r" from="3" to="14" dur="2s" repeatCount="indefinite" />
              <animate attributeName="opacity" from="0.8" to="0" dur="2s" repeatCount="indefinite" />
            </circle>
          </g>
        ))}
      </svg>
    </div>
  );
}

export function Spark({ data, color = "var(--color-cyan)", h = 40 }: { data: number[]; color?: string; h?: number }) {
  const max = Math.max(...data), min = Math.min(...data);
  const w = 120;
  const pts = data.map((v, i) => `${(i / (data.length - 1)) * w},${h - ((v - min) / (max - min || 1)) * h}`).join(" ");
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full" style={{ height: h }}>
      <defs>
        <linearGradient id={`g-${color}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.4" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={`0,${h} ${pts} ${w},${h}`} fill={`url(#g-${color})`} />
      <polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" />
    </svg>
  );
}

export function StatCard({ label, value, delta, data, color = "var(--color-cyan)" }: { label: string; value: string; delta?: string; data?: number[]; color?: string }) {
  const up = delta?.startsWith("+");
  return (
    <div className="glass rounded-xl p-5">
      <div className="flex items-center justify-between text-xs text-muted-foreground"><span className="uppercase tracking-wider">{label}</span>{delta && <span className={up ? "text-success" : "text-destructive"}>{delta}</span>}</div>
      <div className="mt-2 text-3xl font-semibold tracking-tight">{value}</div>
      {data && <div className="mt-3"><Spark data={data} color={color} /></div>}
    </div>
  );
}

export function Section({ title, action, children, className = "" }: { title?: string; action?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <div className={`glass rounded-xl p-5 ${className}`}>
      {title && <div className="mb-4 flex items-center justify-between"><h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">{title}</h3>{action}</div>}
      {children}
    </div>
  );
}

export function Badge({ children, tone = "cyan" }: { children: ReactNode; tone?: "cyan" | "purple" | "success" | "warning" | "danger" }) {
  const map = { cyan: "bg-cyan/10 text-cyan border-cyan/30", purple: "bg-purple/10 text-purple border-purple/30", success: "bg-success/10 text-success border-success/30", warning: "bg-warning/10 text-warning border-warning/30", danger: "bg-destructive/10 text-destructive border-destructive/30" };
  return <span className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-xs font-medium ${map[tone]}`}>{children}</span>;
}

export function NavItem({ to, icon, label }: { to: string; icon: ReactNode; label: string }) {
  return (
    <Link to={to} className="group flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground transition hover:bg-white/5 hover:text-foreground [&.active]:bg-white/10 [&.active]:text-foreground [&.active]:shadow-[inset_2px_0_0_var(--color-cyan)]"
      activeProps={{ className: "active" }}>
      <span className="text-cyan/70 group-hover:text-cyan">{icon}</span>{label}
    </Link>
  );
}
