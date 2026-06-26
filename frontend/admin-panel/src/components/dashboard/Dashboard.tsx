import { Panel, PageHeader, Btn, Pill } from "@/components/ui-x/Panel";
import {
  Activity, Cpu, HardDrive, Zap, AlertTriangle, TrendingUp, Globe2, Users, Brain,
  Bot, FlaskConical, DollarSign, Plus, Play, ShieldAlert, FileText, Sparkles,
  ArrowUpRight, ArrowDownRight,
} from "lucide-react";
import {
  Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, RadialBar, RadialBarChart,
  PolarAngleAxis, BarChart, Bar, CartesianGrid,
} from "recharts";

const accuracySeries = Array.from({ length: 24 }, (_, i) => ({
  t: `${i.toString().padStart(2, "0")}:00`,
  v: 88 + Math.sin(i / 2.4) * 4 + (i > 18 ? 2 : 0),
  c: 84 + Math.cos(i / 3) * 3,
}));

const loadSeries = Array.from({ length: 30 }, (_, i) => ({
  d: i, cpu: 50 + Math.sin(i / 3) * 18 + 6, gpu: 60 + Math.cos(i / 2.5) * 22, mem: 40 + Math.sin(i / 4) * 8,
}));

const forecastBars = [
  { k: "Economic", v: 1240 }, { k: "Climate", v: 980 }, { k: "Political", v: 720 },
  { k: "Trade", v: 640 }, { k: "Energy", v: 510 }, { k: "Health", v: 420 }, { k: "Conflict", v: 310 },
];

const alerts = [
  { t: "CRITICAL", c: "destructive", msg: "Energy grid anomaly detected — Western EU", region: "EU", time: "2m" },
  { t: "WARN", c: "warning", msg: "Forecast confidence drop in Climate Agent #07", region: "Global", time: "6m" },
  { t: "INFO", c: "primary", msg: "Monte Carlo run #18421 completed (10M iterations)", region: "—", time: "11m" },
  { t: "WARN", c: "warning", msg: "API rate limit nearing on GDELT v3 connector", region: "API", time: "18m" },
  { t: "INFO", c: "primary", msg: "New satellite layer ingested from NOAA-21", region: "NA", time: "24m" },
];

const activities = [
  { who: "Dr. K. Müller", act: "deployed model", obj: "geo-llm-v4.2", time: "just now" },
  { who: "Agent.Climate.03", act: "spawned simulation", obj: "sim-2046-A", time: "1m" },
  { who: "M. Tanaka", act: "rotated API key", obj: "noaa-sat-prod", time: "3m" },
  { who: "Treasury Bot", act: "queued forecast", obj: "fx-eur-usd-90d", time: "4m" },
  { who: "S. Okafor", act: "added enterprise", obj: "Helios Defense Corp.", time: "7m" },
  { who: "System", act: "auto-scaled GPUs", obj: "+8 H100 nodes", time: "9m" },
];

const logs = [
  "[12:48:11.221] inference.engine — batch=512 latency=34ms model=geo-llm-v4.2",
  "[12:48:10.984] agent.economic.07 — emitted signal CPI:US delta=+0.12σ",
  "[12:48:10.612] kafka — topic=sim.events partition=4 offset=8821412",
  "[12:48:10.401] ray.worker.31 — task complete monte_carlo iters=200k",
  "[12:48:09.998] postgres — query 12ms rows=842 table=forecasts",
  "[12:48:09.731] gateway — POST /v1/simulate 200 OK key=ent_***x4f1",
  "[12:48:09.402] climate.twin — layer ocean_temp refreshed res=0.25°",
];

export function Dashboard() {
  return (
    <div className="fade-in-up">
      <PageHeader
        eyebrow="Executive Command"
        title="Global Mission Control"
        description="Real-time view across simulations, agents, infrastructure, and intelligence streams."
        actions={
          <>
            <Btn variant="default" size="md"><FileText className="h-3.5 w-3.5" /> Brief</Btn>
            <Btn variant="primary" size="md"><Plus className="h-3.5 w-3.5" /> New Simulation</Btn>
          </>
        }
      />

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3 mb-5">
        <Kpi icon={<Activity />} label="Running Simulations" value="1,284" delta="+12.4%" trend="up" />
        <Kpi icon={<Bot />} label="Active AI Agents" value="9,471" delta="+2.1%" trend="up" />
        <Kpi icon={<TrendingUp />} label="Prediction Accuracy" value="94.2%" delta="+0.6pt" trend="up" />
        <Kpi icon={<AlertTriangle />} label="Global Alerts" value="37" delta="−4" trend="down" tone="warning" />
        <Kpi icon={<DollarSign />} label="MRR (USD)" value="$12.84M" delta="+8.2%" trend="up" />
        <Kpi icon={<Users />} label="Enterprises" value="412" delta="+6" trend="up" />
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-12 gap-5">
        {/* Forecast accuracy chart */}
        <Panel
          accent
          className="col-span-12 xl:col-span-8"
          title="Forecast Accuracy vs Confidence"
          subtitle="24h · rolling window"
          action={
            <div className="flex items-center gap-1">
              {["1H","24H","7D","30D"].map((p, i) => (
                <button key={p} className={`rounded px-2 py-1 font-mono text-[10px] ${i===1 ? "bg-primary/15 text-primary" : "text-muted-foreground hover:bg-surface-2"}`}>{p}</button>
              ))}
            </div>
          }
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={accuracySeries} margin={{ left: -20, right: 8, top: 8, bottom: 0 }}>
                <defs>
                  <linearGradient id="acc" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="oklch(0.82 0.15 210)" stopOpacity={0.5} />
                    <stop offset="100%" stopColor="oklch(0.82 0.15 210)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="conf" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="oklch(0.62 0.20 295)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="oklch(0.62 0.20 295)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="oklch(0.32 0.04 260 / 30%)" vertical={false} />
                <XAxis dataKey="t" stroke="oklch(0.68 0.025 255)" fontSize={10} tickLine={false} axisLine={false} interval={3} />
                <YAxis stroke="oklch(0.68 0.025 255)" fontSize={10} tickLine={false} axisLine={false} domain={[78, 100]} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.04 260)", border: "1px solid oklch(0.32 0.04 260)", borderRadius: 8, fontSize: 11 }} />
                <Area type="monotone" dataKey="v" stroke="oklch(0.82 0.15 210)" strokeWidth={2} fill="url(#acc)" />
                <Area type="monotone" dataKey="c" stroke="oklch(0.62 0.20 295)" strokeWidth={2} fill="url(#conf)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-2 flex items-center gap-4 text-xs">
            <Legend dot="oklch(0.82 0.15 210)" label="Accuracy" />
            <Legend dot="oklch(0.62 0.20 295)" label="Confidence Index" />
          </div>
        </Panel>

        {/* System Vitals radial */}
        <Panel className="col-span-12 sm:col-span-6 xl:col-span-4" title="System Vitals" subtitle="Cluster aggregate">
          <div className="grid grid-cols-2 gap-3">
            <Vital label="CPU" value={62} color="oklch(0.82 0.15 210)" icon={<Cpu className="h-3 w-3" />} />
            <Vital label="GPU" value={81} color="oklch(0.62 0.20 295)" icon={<Zap className="h-3 w-3" />} />
            <Vital label="MEM" value={44} color="oklch(0.74 0.17 155)" icon={<Activity className="h-3 w-3" />} />
            <Vital label="DISK" value={58} color="oklch(0.80 0.16 80)" icon={<HardDrive className="h-3 w-3" />} />
          </div>
        </Panel>

        {/* Global Map */}
        <Panel className="col-span-12 xl:col-span-8" title="Global Operations Map" subtitle="Live · 184 regions · 2,041 nodes" action={<Pill tone="success">STREAMING</Pill>}>
          <GlobalMap />
        </Panel>

        {/* Threat & Risk */}
        <Panel className="col-span-12 sm:col-span-6 xl:col-span-4" title="Threat & Risk Posture">
          <div className="space-y-4">
            <RiskMeter label="Global Risk Index" value={42} max={100} tone="warning" note="Moderate · trending ↗" />
            <RiskMeter label="Threat Level" value={2} max={5} tone="warning" note="DEFCON-equivalent" />
            <RiskMeter label="System Integrity" value={97} max={100} tone="success" note="All gates pass" />
            <RiskMeter label="Data Freshness" value={91} max={100} tone="primary" note="ETL nominal" />
          </div>
        </Panel>

        {/* Load */}
        <Panel className="col-span-12 xl:col-span-8" title="Compute Load · last 30 min" action={<Pill tone="primary">AUTO-SCALE</Pill>}>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={loadSeries} margin={{ left: -20, right: 8, top: 8, bottom: 0 }}>
                <defs>
                  <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="oklch(0.82 0.15 210)" stopOpacity={0.4}/><stop offset="100%" stopColor="oklch(0.82 0.15 210)" stopOpacity={0}/></linearGradient>
                  <linearGradient id="g2" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="oklch(0.62 0.20 295)" stopOpacity={0.4}/><stop offset="100%" stopColor="oklch(0.62 0.20 295)" stopOpacity={0}/></linearGradient>
                </defs>
                <CartesianGrid stroke="oklch(0.32 0.04 260 / 30%)" vertical={false} />
                <XAxis dataKey="d" hide />
                <YAxis stroke="oklch(0.68 0.025 255)" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.04 260)", border: "1px solid oklch(0.32 0.04 260)", borderRadius: 8, fontSize: 11 }} />
                <Area dataKey="cpu" stroke="oklch(0.82 0.15 210)" fill="url(#g1)" strokeWidth={1.5} />
                <Area dataKey="gpu" stroke="oklch(0.62 0.20 295)" fill="url(#g2)" strokeWidth={1.5} />
                <Area dataKey="mem" stroke="oklch(0.74 0.17 155)" fill="transparent" strokeWidth={1.5} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Forecasts by domain */}
        <Panel className="col-span-12 sm:col-span-6 xl:col-span-4" title="Daily Forecasts · by domain">
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={forecastBars} margin={{ left: -20, right: 8, top: 8, bottom: 0 }}>
                <CartesianGrid stroke="oklch(0.32 0.04 260 / 30%)" vertical={false} />
                <XAxis dataKey="k" stroke="oklch(0.68 0.025 255)" fontSize={9} tickLine={false} axisLine={false} />
                <YAxis stroke="oklch(0.68 0.025 255)" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.04 260)", border: "1px solid oklch(0.32 0.04 260)", borderRadius: 8, fontSize: 11 }} />
                <Bar dataKey="v" fill="oklch(0.82 0.15 210)" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Alerts */}
        <Panel className="col-span-12 xl:col-span-5" title="Global Alerts" subtitle="Last 30 minutes" action={<Btn variant="ghost" size="sm">View all</Btn>}>
          <ul className="space-y-2">
            {alerts.map((a, i) => (
              <li key={i} className="flex items-start gap-3 rounded-md bg-background/30 p-2.5">
                <Pill tone={a.c as any}>{a.t}</Pill>
                <div className="flex-1 min-w-0">
                  <div className="text-sm">{a.msg}</div>
                  <div className="font-mono text-[10px] text-muted-foreground mt-0.5">region · {a.region}</div>
                </div>
                <div className="font-mono text-[10px] text-muted-foreground">{a.time}</div>
              </li>
            ))}
          </ul>
        </Panel>

        {/* Live logs */}
        <Panel className="col-span-12 xl:col-span-4" title="Live Logs" subtitle="stream://wynthora.core" action={<Pill tone="success"><span className="h-1 w-1 rounded-full bg-success pulse-dot"/> LIVE</Pill>}>
          <div className="rounded-md bg-black/40 border border-border/50 p-3 font-mono text-[10.5px] leading-relaxed text-muted-foreground/90 scanline">
            {logs.map((l, i) => (
              <div key={i} className={i === 0 ? "text-success" : ""}>{l}</div>
            ))}
          </div>
        </Panel>

        {/* Activity */}
        <Panel className="col-span-12 xl:col-span-3" title="Recent Activity">
          <ul className="space-y-3">
            {activities.map((a, i) => (
              <li key={i} className="flex items-start gap-2.5 text-sm">
                <div className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-secondary/20 text-secondary font-mono text-[10px] font-bold">
                  {a.who.split(" ").map(x=>x[0]).slice(0,2).join("")}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="truncate"><span className="font-medium">{a.who}</span> <span className="text-muted-foreground">{a.act}</span> <span className="font-mono text-[11px] text-primary">{a.obj}</span></div>
                  <div className="font-mono text-[10px] text-muted-foreground">{a.time} ago</div>
                </div>
              </li>
            ))}
          </ul>
        </Panel>

        {/* Quick actions */}
        <Panel className="col-span-12 sm:col-span-6 xl:col-span-4" title="Quick Actions">
          <div className="grid grid-cols-2 gap-2">
            {[
              { i: <Play className="h-4 w-4" />, l: "Run Simulation" },
              { i: <Brain className="h-4 w-4" />, l: "Deploy Model" },
              { i: <Globe2 className="h-4 w-4" />, l: "Open Digital Twin" },
              { i: <ShieldAlert className="h-4 w-4" />, l: "Trigger Drill" },
              { i: <FlaskConical className="h-4 w-4" />, l: "Monte Carlo" },
              { i: <Sparkles className="h-4 w-4" />, l: "AI Insight" },
            ].map((q) => (
              <button key={q.l} className="group flex items-center gap-2 rounded-md glass px-3 py-2.5 text-sm hover:glow-cyan transition-all text-left">
                <span className="text-primary group-hover:scale-110 transition-transform">{q.i}</span>
                <span className="flex-1 truncate">{q.l}</span>
                <ArrowUpRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
              </button>
            ))}
          </div>
        </Panel>

        {/* Pinned widgets / Recent reports */}
        <Panel className="col-span-12 sm:col-span-6 xl:col-span-4" title="Pinned Widgets">
          <div className="grid grid-cols-2 gap-2">
            {[
              { l: "USD/EUR 90d", v: "1.087", d: "+0.4%" },
              { l: "Atlantic SST", v: "+1.2°C", d: "+0.1°" },
              { l: "Brent Crude", v: "$84.21", d: "−1.1%" },
              { l: "Geo-risk: SCS", v: "Elevated", d: "↗" },
            ].map((p) => (
              <div key={p.l} className="rounded-md bg-background/40 p-3">
                <div className="font-mono text-[10px] uppercase text-muted-foreground">{p.l}</div>
                <div className="mt-1 font-display text-lg font-semibold">{p.v}</div>
                <div className="font-mono text-[10px] text-primary">{p.d}</div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel className="col-span-12 xl:col-span-4" title="Recent Reports">
          <ul className="divide-y divide-border/50">
            {[
              { n: "Q4 Global Economic Outlook", t: "Executive", d: "2h" },
              { n: "Atlantic Hurricane Probability", t: "Climate", d: "5h" },
              { n: "Indo-Pacific Trade Disruption", t: "Geopolitics", d: "1d" },
              { n: "Energy Grid Stress · EU", t: "Energy", d: "2d" },
            ].map((r) => (
              <li key={r.n} className="flex items-center justify-between py-2.5">
                <div className="min-w-0">
                  <div className="text-sm font-medium truncate">{r.n}</div>
                  <div className="font-mono text-[10px] text-muted-foreground">{r.t} · {r.d} ago</div>
                </div>
                <Btn variant="ghost" size="sm"><ArrowUpRight className="h-3.5 w-3.5" /></Btn>
              </li>
            ))}
          </ul>
        </Panel>
      </div>
    </div>
  );
}

function Kpi({ icon, label, value, delta, trend, tone = "primary" }: { icon: React.ReactNode; label: string; value: string; delta: string; trend: "up" | "down"; tone?: "primary" | "warning" }) {
  return (
    <div className="relative rounded-xl glass p-3.5 overflow-hidden">
      <div className="pointer-events-none absolute -right-6 -top-6 h-20 w-20 rounded-full bg-primary/10 blur-2xl" />
      <div className="flex items-center justify-between">
        <span className={`grid h-7 w-7 place-items-center rounded-md ${tone === "warning" ? "bg-warning/15 text-warning" : "bg-primary/15 text-primary"}`}>
          {icon}
        </span>
        <span className={`flex items-center gap-0.5 font-mono text-[10px] ${trend === "up" ? "text-success" : "text-destructive"}`}>
          {trend === "up" ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
          {delta}
        </span>
      </div>
      <div className="mt-2 font-display text-xl font-bold tracking-tight">{value}</div>
      <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">{label}</div>
    </div>
  );
}

function Vital({ label, value, color, icon }: { label: string; value: number; color: string; icon: React.ReactNode }) {
  return (
    <div className="rounded-lg bg-background/40 p-3 flex items-center gap-3">
      <div className="relative h-16 w-16 shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart innerRadius="70%" outerRadius="100%" data={[{ v: value }]} startAngle={90} endAngle={-270}>
            <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
            <RadialBar dataKey="v" fill={color} cornerRadius={8} background={{ fill: "oklch(0.26 0.035 262)" }} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 grid place-items-center font-mono text-xs font-semibold">{value}%</div>
      </div>
      <div>
        <div className="flex items-center gap-1 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">{icon}{label}</div>
        <div className="text-[11px] text-foreground/80">{value < 50 ? "Healthy" : value < 80 ? "Steady" : "High"}</div>
      </div>
    </div>
  );
}

function Legend({ dot, label }: { dot: string; label: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className="h-2 w-2 rounded-full" style={{ background: dot, boxShadow: `0 0 8px ${dot}` }} />
      <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">{label}</span>
    </div>
  );
}

function RiskMeter({ label, value, max, tone, note }: { label: string; value: number; max: number; tone: "success" | "warning" | "primary"; note: string }) {
  const pct = (value / max) * 100;
  const colors = { success: "oklch(0.74 0.17 155)", warning: "oklch(0.80 0.16 80)", primary: "oklch(0.82 0.15 210)" };
  return (
    <div>
      <div className="flex items-baseline justify-between mb-1.5">
        <span className="text-sm">{label}</span>
        <span className="font-mono text-xs">
          <span className="font-semibold" style={{ color: colors[tone] }}>{value}</span>
          <span className="text-muted-foreground">/{max}</span>
        </span>
      </div>
      <div className="h-1.5 w-full rounded-full bg-background/60 overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: colors[tone], boxShadow: `0 0 12px ${colors[tone]}` }} />
      </div>
      <div className="mt-1 font-mono text-[10px] text-muted-foreground">{note}</div>
    </div>
  );
}

function GlobalMap() {
  // Stylized dotted world map with active nodes
  const nodes = [
    { x: 22, y: 38, n: "NA-EAST", s: "primary" },
    { x: 18, y: 50, n: "NA-WEST", s: "success" },
    { x: 35, y: 70, n: "SA-1", s: "primary" },
    { x: 48, y: 32, n: "EU-CTRL", s: "warning" },
    { x: 54, y: 42, n: "ME-1", s: "success" },
    { x: 62, y: 55, n: "AF-1", s: "primary" },
    { x: 72, y: 38, n: "AS-IN", s: "success" },
    { x: 82, y: 40, n: "AS-CN", s: "warning" },
    { x: 88, y: 62, n: "OC-1", s: "primary" },
    { x: 50, y: 22, n: "ARCTIC", s: "primary" },
  ];
  const colorOf = (s: string) => s === "warning" ? "oklch(0.80 0.16 80)" : s === "success" ? "oklch(0.74 0.17 155)" : "oklch(0.82 0.15 210)";
  return (
    <div className="relative h-72 sm:h-80 w-full overflow-hidden rounded-lg grid-bg bg-background/30">
      {/* dotted continents */}
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute inset-0 h-full w-full opacity-50">
        {Array.from({ length: 28 * 14 }).map((_, i) => {
          const x = (i % 28) * 3.6 + 1;
          const y = Math.floor(i / 28) * 7 + 4;
          // crude continent mask
          const inLand =
            (x > 12 && x < 36 && y > 18 && y < 70 && Math.sin(x/6 + y/9) > -0.2) ||
            (x > 44 && x < 62 && y > 16 && y < 70 && Math.cos(x/8 + y/7) > -0.2) ||
            (x > 64 && x < 92 && y > 18 && y < 72 && Math.sin(x/5 + y/8) > -0.3);
          if (!inLand) return null;
          return <circle key={i} cx={x} cy={y} r={0.55} fill="oklch(0.82 0.15 210)" opacity={0.5} />;
        })}
      </svg>

      {/* arcs */}
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute inset-0 h-full w-full">
        <defs>
          <linearGradient id="arc" x1="0" x2="1">
            <stop offset="0%" stopColor="oklch(0.82 0.15 210)" stopOpacity="0.1"/>
            <stop offset="50%" stopColor="oklch(0.82 0.15 210)" stopOpacity="0.9"/>
            <stop offset="100%" stopColor="oklch(0.62 0.20 295)" stopOpacity="0.1"/>
          </linearGradient>
        </defs>
        {[
          [22,38,48,32], [48,32,72,38], [72,38,88,62], [22,38,72,38], [54,42,62,55],
        ].map(([x1,y1,x2,y2], i) => {
          const cx = (x1+x2)/2, cy = Math.min(y1,y2) - 14;
          return <path key={i} d={`M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`} fill="none" stroke="url(#arc)" strokeWidth={0.3} />;
        })}
      </svg>

      {/* nodes */}
      {nodes.map((n) => (
        <div key={n.n} className="absolute -translate-x-1/2 -translate-y-1/2" style={{ left: `${n.x}%`, top: `${n.y}%` }}>
          <div className="relative">
            <span className="absolute inset-0 -m-1.5 rounded-full animate-ping" style={{ background: colorOf(n.s), opacity: 0.3 }} />
            <span className="block h-2 w-2 rounded-full" style={{ background: colorOf(n.s), boxShadow: `0 0 10px ${colorOf(n.s)}` }} />
          </div>
          <div className="absolute left-3 top-1/2 -translate-y-1/2 font-mono text-[9px] text-muted-foreground whitespace-nowrap">{n.n}</div>
        </div>
      ))}

      {/* legend */}
      <div className="absolute bottom-3 left-3 flex items-center gap-3 rounded-md glass px-2.5 py-1.5">
        <Legend dot="oklch(0.74 0.17 155)" label="Nominal" />
        <Legend dot="oklch(0.80 0.16 80)" label="Watch" />
        <Legend dot="oklch(0.82 0.15 210)" label="Active" />
      </div>
      <div className="absolute top-3 right-3 font-mono text-[10px] text-muted-foreground">LAT 0.0° · LON 0.0° · 1:1 PROJ</div>
    </div>
  );
}
