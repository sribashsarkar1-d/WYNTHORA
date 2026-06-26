import { Search, Bell, Command, Globe, ShieldAlert, Zap } from "lucide-react";

export function Topbar() {
  return (
    <header className="sticky top-0 z-30 h-16 border-b border-border bg-background/60 backdrop-blur-xl">
      <div className="flex h-full items-center gap-4 px-4 sm:px-6">
        {/* Search / command */}
        <div className="flex-1 max-w-xl">
          <div className="group flex items-center gap-2 rounded-lg glass px-3 py-2 transition-all focus-within:glow-cyan">
            <Search className="h-4 w-4 text-muted-foreground" />
            <input
              placeholder="Search simulations, agents, users, datasets…"
              className="flex-1 bg-transparent text-sm placeholder:text-muted-foreground/60 focus:outline-none"
            />
            <kbd className="hidden sm:flex items-center gap-1 rounded border border-border bg-background/50 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
              <Command className="h-3 w-3" /> K
            </kbd>
          </div>
        </div>

        {/* Live status pills */}
        <div className="hidden xl:flex items-center gap-2">
          <StatusPill icon={<Globe className="h-3 w-3" />} label="GLOBAL" value="NOMINAL" tone="success" />
          <StatusPill icon={<ShieldAlert className="h-3 w-3" />} label="THREAT" value="LVL 2" tone="warning" />
          <StatusPill icon={<Zap className="h-3 w-3" />} label="LATENCY" value="34ms" tone="muted" />
        </div>

        {/* Actions */}
        <button className="relative grid h-9 w-9 place-items-center rounded-lg glass hover:glow-cyan transition-all">
          <Bell className="h-4 w-4" />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-destructive" />
        </button>

        <div className="flex items-center gap-2.5 rounded-lg glass px-2 py-1.5">
          <div className="grid h-7 w-7 place-items-center rounded-md bg-[var(--gradient-aurora)] text-xs font-bold text-primary-foreground">
            AX
          </div>
          <div className="hidden sm:block leading-tight pr-1">
            <div className="text-xs font-semibold">Alex Chen</div>
            <div className="font-mono text-[10px] text-muted-foreground">SUPER ADMIN</div>
          </div>
        </div>
      </div>
    </header>
  );
}

function StatusPill({
  icon, label, value, tone,
}: { icon: React.ReactNode; label: string; value: string; tone: "success" | "warning" | "muted" }) {
  const toneClass =
    tone === "success" ? "text-success" : tone === "warning" ? "text-warning" : "text-muted-foreground";
  return (
    <div className="flex items-center gap-1.5 rounded-md glass px-2.5 py-1.5">
      <span className={toneClass}>{icon}</span>
      <span className="font-mono text-[10px] text-muted-foreground">{label}</span>
      <span className={`font-mono text-[10px] font-semibold ${toneClass}`}>{value}</span>
    </div>
  );
}
