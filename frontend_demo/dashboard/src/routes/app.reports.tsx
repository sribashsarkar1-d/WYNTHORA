import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Download, FileText } from "lucide-react";

export const Route = createFileRoute("/app/reports")({ component: Reports });

function Reports() {
  const reports = [
    ["Q4 Global Macro Outlook", "Executive", "2025-12-04", "PDF"],
    ["EU-CN Trade Cascade Brief", "Sovereign", "2025-12-03", "PDF"],
    ["Climate Stress Test 2030", "Research", "2025-12-01", "XLSX"],
    ["Hedge Book Rebalance Memo", "Internal", "2025-11-28", "PDF"],
    ["LatAm Political Risk Pack", "Executive", "2025-11-25", "PDF"],
  ];
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Briefings · Exports · Scheduling</p><h1 className="font-display text-3xl font-bold">Reports Center</h1></div>
        <button className="rounded-lg bg-gradient-to-r from-cyan to-purple px-4 py-2 text-sm font-semibold text-background">+ New report</button>
      </div>
      <div className="grid gap-3 md:grid-cols-3">
        {[["Executive PDF", "Board-ready, 1-page"], ["Analyst XLSX", "Raw data + assumptions"], ["Scheduled feed", "Daily, weekly, on-event"]].map(([t, d]) => (
          <div key={t} className="glass rounded-xl p-5">
            <FileText className="h-5 w-5 text-cyan" />
            <div className="mt-3 font-semibold">{t}</div>
            <div className="text-xs text-muted-foreground">{d}</div>
          </div>
        ))}
      </div>
      <Section title="Recent reports">
        <table className="w-full text-sm">
          <thead className="text-xs uppercase tracking-wider text-muted-foreground"><tr className="border-b border-border"><th className="py-2 text-left">Title</th><th>Audience</th><th>Date</th><th>Format</th><th></th></tr></thead>
          <tbody>
            {reports.map(([t, a, d, f]) => (
              <tr key={t} className="border-b border-border/50">
                <td className="py-3 font-medium">{t}</td>
                <td className="text-center"><Badge tone={a === "Sovereign" ? "purple" : a === "Executive" ? "cyan" : "success"}>{a}</Badge></td>
                <td className="text-center font-mono text-muted-foreground">{d}</td>
                <td className="text-center font-mono">{f}</td>
                <td className="text-right"><button className="rounded-md border border-border p-1.5 hover:border-cyan/40"><Download className="h-3.5 w-3.5" /></button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
