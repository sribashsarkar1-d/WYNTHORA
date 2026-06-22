import { createFileRoute, Link, Outlet } from "@tanstack/react-router";
import { Activity, Bot, Boxes, Brain, CircleDot, Cloud, Cpu, Database, FileText, Globe2, LayoutDashboard, LineChart, Map, Network, Search, Settings, Shield, ShieldAlert, TrendingUp, Users, Bell, Sparkles, Workflow, Vote } from "lucide-react";
import { NavItem } from "@/components/wynthora";

export const Route = createFileRoute("/app")({ component: Shell });

function Shell() {
  return (
    <div className="flex min-h-screen">
      <aside className="glass-strong sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border lg:flex">
        <div className="flex items-center gap-2 border-b border-border px-5 py-4">
          <div className="grid h-8 w-8 place-items-center rounded-md bg-gradient-to-br from-cyan to-purple"><Globe2 className="h-4 w-4 text-background" /></div>
          <div><div className="text-sm font-bold tracking-wider">WYNTHORA</div><div className="text-[10px] uppercase tracking-widest text-muted-foreground">Sim Engine v4.2</div></div>
        </div>
        <nav className="flex-1 space-y-0.5 overflow-y-auto p-3 text-sm">
          <div className="px-2 pb-1 pt-2 text-[10px] uppercase tracking-widest text-muted-foreground">Core</div>
          <NavItem to="/app/dashboard" icon={<LayoutDashboard className="h-4 w-4" />} label="Dashboard" />
          <NavItem to="/app/ai" icon={<Bot className="h-4 w-4" />} label="AI Command Center" />
          <NavItem to="/app/scenario" icon={<Workflow className="h-4 w-4" />} label="Scenario Builder" />
          <NavItem to="/app/simulation" icon={<Cpu className="h-4 w-4" />} label="Live Simulation" />
          <NavItem to="/app/results" icon={<LineChart className="h-4 w-4" />} label="Predictions" />
          <div className="px-2 pb-1 pt-4 text-[10px] uppercase tracking-widest text-muted-foreground">Intelligence</div>
          <NavItem to="/app/risk" icon={<ShieldAlert className="h-4 w-4" />} label="Risk Center" />
          <NavItem to="/app/world" icon={<Map className="h-4 w-4" />} label="World Map" />
          <NavItem to="/app/economy" icon={<TrendingUp className="h-4 w-4" />} label="Economy" />
          <NavItem to="/app/climate" icon={<Cloud className="h-4 w-4" />} label="Climate" />
          <NavItem to="/app/politics" icon={<Vote className="h-4 w-4" />} label="Politics" />
          <NavItem to="/app/trade" icon={<Boxes className="h-4 w-4" />} label="Trade & Supply" />
          <div className="px-2 pb-1 pt-4 text-[10px] uppercase tracking-widest text-muted-foreground">Engine</div>
          <NavItem to="/app/agents" icon={<Network className="h-4 w-4" />} label="Multi-Agent" />
          <NavItem to="/app/monte-carlo" icon={<Activity className="h-4 w-4" />} label="Monte Carlo" />
          <div className="px-2 pb-1 pt-4 text-[10px] uppercase tracking-widest text-muted-foreground">Workspace</div>
          <NavItem to="/app/reports" icon={<FileText className="h-4 w-4" />} label="Reports" />
          <NavItem to="/app/notifications" icon={<Bell className="h-4 w-4" />} label="Notifications" />
          <NavItem to="/app/admin" icon={<Shield className="h-4 w-4" />} label="Admin" />
          <NavItem to="/app/settings" icon={<Settings className="h-4 w-4" />} label="Settings" />
          <NavItem to="/app/design-system" icon={<Sparkles className="h-4 w-4" />} label="Design System" />
        </nav>
        <div className="border-t border-border p-3">
          <div className="glass flex items-center gap-3 rounded-lg p-2.5">
            <div className="grid h-8 w-8 place-items-center rounded-full bg-gradient-to-br from-cyan to-purple text-xs font-bold text-background">JC</div>
            <div className="min-w-0"><div className="truncate text-xs font-medium">Dr. J. Chen</div><div className="truncate text-[10px] text-muted-foreground">Sovereign Analyst</div></div>
            <CircleDot className="ml-auto h-3 w-3 text-success" />
          </div>
        </div>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="glass-strong sticky top-0 z-10 flex h-14 items-center gap-3 border-b border-border px-4 lg:px-6">
          <div className="relative flex-1 max-w-xl">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input className="h-9 w-full rounded-lg border border-border bg-input/50 pl-9 pr-3 text-sm placeholder:text-muted-foreground focus:border-cyan/50 focus:outline-none" placeholder="Ask the engine… 'forecast EUR/USD if Brent breaches $120'" />
          </div>
          <button className="glass hidden items-center gap-2 rounded-lg px-3 py-1.5 text-xs md:flex"><Database className="h-3 w-3 text-cyan" /> 184 sources live</button>
          <button className="glass hidden items-center gap-2 rounded-lg px-3 py-1.5 text-xs md:flex"><Brain className="h-3 w-3 text-purple" /> 42 agents</button>
          <Link to="/app/notifications" className="glass relative grid h-9 w-9 place-items-center rounded-lg"><Bell className="h-4 w-4" /><span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-destructive" /></Link>
        </header>
        <main className="flex-1 p-4 lg:p-6"><Outlet /></main>
      </div>
    </div>
  );
}
