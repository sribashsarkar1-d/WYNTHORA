import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge, StatCard } from "@/components/wynthora";

export const Route = createFileRoute("/app/admin")({ component: Admin });

const s = (n: number) => Array.from({ length: 24 }, (_, i) => 50 + Math.sin(i / 2 + n) * 20);

function Admin() {
  return (
    <div className="space-y-4">
      <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Tenant administration</p><h1 className="font-display text-3xl font-bold">Admin Panel</h1></div>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Users" value="284" delta="+12" data={s(1)} />
        <StatCard label="API calls (24h)" value="14.2M" delta="+8%" data={s(2)} color="var(--color-purple)" />
        <StatCard label="Sources online" value="184 / 187" data={s(3)} color="var(--color-success)" />
        <StatCard label="Compute usage" value="78%" delta="+4%" data={s(4)} color="var(--color-warning)" />
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <Section title="Users">
          <table className="w-full text-sm">
            <thead className="text-xs text-muted-foreground"><tr><th className="text-left">Name</th><th>Role</th><th>Status</th></tr></thead>
            <tbody>
              {[["Dr. J. Chen", "Admin", "active"], ["A. Iversen", "Analyst", "active"], ["R. Maddox", "Strategic", "active"], ["S. Park", "Read-only", "invited"], ["L. Okafor", "Analyst", "suspended"]].map(([n, r, s]) => (
                <tr key={n} className="border-b border-border/50"><td className="py-2.5">{n}</td><td className="text-center text-muted-foreground">{r}</td><td className="text-center"><Badge tone={s === "active" ? "success" : s === "invited" ? "cyan" : "warning"}>{s}</Badge></td></tr>
              ))}
            </tbody>
          </table>
        </Section>
        <Section title="Roles & permissions">
          <ul className="space-y-2 text-sm">
            {[["Sovereign Admin", "Full access · audit · billing"], ["Analyst", "Run sims · view reports"], ["Strategic", "Read briefings · receive alerts"], ["Read-only", "Dashboards only"]].map(([r, d]) => (
              <li key={r} className="glass rounded-lg p-3"><div className="font-semibold">{r}</div><div className="text-xs text-muted-foreground">{d}</div></li>
            ))}
          </ul>
        </Section>
        <Section title="Data sources">
          <ul className="space-y-1 text-xs">
            {[["Bloomberg Terminal", "ok"], ["Reuters Feed", "ok"], ["NOAA Sat", "ok"], ["IMF DataMapper", "ok"], ["NATO SitRep", "degraded"], ["Sentinel-2", "ok"]].map(([n, s]) => (
              <li key={n} className="flex justify-between border-b border-border py-1.5"><span>{n}</span><Badge tone={s === "ok" ? "success" : "warning"}>{s}</Badge></li>
            ))}
          </ul>
        </Section>
        <Section title="System monitoring">
          <div className="space-y-3 text-xs">
            {[["CPU", 64], ["GPU", 91], ["Memory", 58], ["Network", 42], ["Disk I/O", 31]].map(([l, v]) => (
              <div key={l as string}><div className="mb-1 flex justify-between"><span>{l}</span><span className="font-mono text-muted-foreground">{v}%</span></div><div className="h-1.5 rounded-full bg-muted overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-cyan to-purple" style={{ width: `${v}%` }} /></div></div>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
