import { Link, useRouterState } from "@tanstack/react-router";
import {
  LayoutDashboard, Users, Shield, Building2, Brain, Bot, FlaskConical, Database,
  LineChart, Dices, Globe2, Radar, Network, HardDrive, Server, Lock, CreditCard,
  Bell, FileText, Settings, Activity, Palette, ChevronRight, Sparkles,
} from "lucide-react";

type Item = { to: string; label: string; icon: any; badge?: string };
type Group = { label: string; items: Item[] };

const groups: Group[] = [
  {
    label: "Command",
    items: [
      { to: "/", label: "Executive Dashboard", icon: LayoutDashboard },
      { to: "/activity", label: "Activity Center", icon: Activity },
      { to: "/intelligence", label: "Intelligence Center", icon: Radar, badge: "LIVE" },
    ],
  },
  {
    label: "Access",
    items: [
      { to: "/users", label: "User Management", icon: Users },
      { to: "/roles", label: "Roles & Permissions", icon: Shield },
      { to: "/organizations", label: "Organizations", icon: Building2 },
    ],
  },
  {
    label: "AI Core",
    items: [
      { to: "/models", label: "AI Models", icon: Brain },
      { to: "/agents", label: "Multi-Agent Mgmt", icon: Bot },
      { to: "/simulations", label: "Simulations", icon: FlaskConical },
      { to: "/forecast", label: "Forecast Engine", icon: LineChart },
      { to: "/monte-carlo", label: "Monte Carlo", icon: Dices },
      { to: "/digital-twin", label: "Digital Twin Earth", icon: Globe2, badge: "3D" },
    ],
  },
  {
    label: "Infrastructure",
    items: [
      { to: "/data-sources", label: "Data Sources", icon: Database },
      { to: "/api-gateway", label: "API Gateway", icon: Network },
      { to: "/databases", label: "Databases", icon: HardDrive },
      { to: "/infrastructure", label: "Infrastructure", icon: Server },
      { to: "/security", label: "Security Center", icon: Lock },
    ],
  },
  {
    label: "Operations",
    items: [
      { to: "/billing", label: "Billing", icon: CreditCard },
      { to: "/notifications", label: "Notifications", icon: Bell },
      { to: "/reports", label: "Reports", icon: FileText },
      { to: "/settings", label: "Settings", icon: Settings },
      { to: "/design-system", label: "Design System", icon: Palette },
    ],
  },
];

export function AppSidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <aside className="hidden lg:flex w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar/80 backdrop-blur-xl">
      <div className="flex h-16 items-center gap-2.5 border-b border-sidebar-border px-5">
        <div className="relative grid h-9 w-9 place-items-center rounded-lg bg-[var(--gradient-aurora)] glow-cyan">
          <Sparkles className="h-4.5 w-4.5 text-primary-foreground" />
        </div>
        <div className="min-w-0">
          <div className="font-display text-sm font-bold tracking-wide gradient-text">WYNTHORA</div>
          <div className="font-mono text-[10px] text-muted-foreground">SIMULATION ENGINE v4.2</div>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {groups.map((g) => (
          <div key={g.label} className="mb-5">
            <div className="px-2 mb-1.5 font-mono text-[10px] uppercase tracking-[0.15em] text-muted-foreground/70">
              {g.label}
            </div>
            <div className="space-y-0.5">
              {g.items.map((item) => {
                const active = pathname === item.to;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    className={`group relative flex items-center gap-2.5 rounded-md px-2.5 py-2 text-sm transition-all ${
                      active
                        ? "bg-sidebar-accent text-sidebar-accent-foreground"
                        : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
                    }`}
                  >
                    {active && (
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 h-5 w-0.5 rounded-r bg-primary glow-cyan" />
                    )}
                    <Icon className={`h-4 w-4 shrink-0 ${active ? "text-primary" : ""}`} />
                    <span className="flex-1 truncate">{item.label}</span>
                    {item.badge && (
                      <span className="rounded-sm bg-primary/15 px-1.5 py-0.5 font-mono text-[9px] font-semibold text-primary">
                        {item.badge}
                      </span>
                    )}
                    {active && <ChevronRight className="h-3 w-3 opacity-60" />}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      <div className="border-t border-sidebar-border p-3">
        <div className="rounded-lg glass p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">System</span>
            <span className="flex items-center gap-1.5 text-[10px] font-mono text-success">
              <span className="h-1.5 w-1.5 rounded-full bg-success pulse-dot" /> OPERATIONAL
            </span>
          </div>
          <div className="grid grid-cols-3 gap-1.5 text-center">
            {[["CPU","62%"],["GPU","81%"],["MEM","44%"]].map(([k,v]) => (
              <div key={k} className="rounded bg-background/40 px-1 py-1.5">
                <div className="font-mono text-[9px] text-muted-foreground">{k}</div>
                <div className="font-mono text-[11px] font-semibold text-foreground">{v}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
}
