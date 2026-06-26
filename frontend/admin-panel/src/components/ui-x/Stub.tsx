import { Panel, PageHeader, Btn, Pill } from "./Panel";
import { Download, Plus, Filter, Search, MoreHorizontal, ArrowUpRight } from "lucide-react";
import type { ReactNode } from "react";

export function ModulePage({
  eyebrow, title, description, sections,
}: {
  eyebrow: string;
  title: string;
  description: string;
  sections: { label: string; items: string[] }[];
}) {
  return (
    <div className="fade-in-up">
      <PageHeader
        eyebrow={eyebrow}
        title={title}
        description={description}
        actions={
          <>
            <Btn variant="default" size="md"><Download className="h-3.5 w-3.5" /> Export</Btn>
            <Btn variant="primary" size="md"><Plus className="h-3.5 w-3.5" /> New</Btn>
          </>
        }
      />

      {/* Toolbar */}
      <Panel padded={false} className="mb-5">
        <div className="flex flex-wrap items-center gap-2 p-3">
          <div className="flex items-center gap-2 rounded-md bg-background/40 px-2.5 py-1.5 flex-1 min-w-[220px]">
            <Search className="h-3.5 w-3.5 text-muted-foreground" />
            <input placeholder="Search…" className="flex-1 bg-transparent text-sm focus:outline-none placeholder:text-muted-foreground/60" />
          </div>
          <Btn variant="default" size="sm"><Filter className="h-3 w-3" /> Filters</Btn>
          <Btn variant="default" size="sm">Status: All</Btn>
          <Btn variant="default" size="sm">Region: Global</Btn>
          <Btn variant="default" size="sm">Last 7 days</Btn>
        </div>
      </Panel>

      {/* Capability sections */}
      <div className="grid gap-5 lg:grid-cols-2">
        {sections.map((sec) => (
          <Panel key={sec.label} title={sec.label} subtitle={`${sec.items.length} capabilities`} action={<Btn variant="ghost" size="sm"><MoreHorizontal className="h-3.5 w-3.5" /></Btn>}>
            <ul className="divide-y divide-border/50">
              {sec.items.map((it, i) => (
                <li key={it} className="flex items-center justify-between py-2.5">
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="grid h-7 w-7 shrink-0 place-items-center rounded-md bg-primary/10 font-mono text-[10px] font-semibold text-primary">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <div className="min-w-0">
                      <div className="text-sm font-medium truncate">{it}</div>
                      <div className="font-mono text-[10px] text-muted-foreground">module.{slug(it)}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Pill tone={pickTone(i)}>{pickStatus(i)}</Pill>
                    <Btn variant="ghost" size="sm"><ArrowUpRight className="h-3.5 w-3.5" /></Btn>
                  </div>
                </li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>

      <p className="mt-6 text-center text-xs text-muted-foreground">
        Module scaffold — wire data sources to populate live tables, charts, and detail drawers.
      </p>
    </div>
  );
}

function slug(s: string) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "_"); }
function pickTone(i: number): "success" | "primary" | "warning" | "secondary" | "muted" {
  const o = ["success","primary","warning","secondary","muted"] as const; return o[i % o.length];
}
function pickStatus(i: number) {
  const o = ["ACTIVE","READY","QUEUED","PENDING","IDLE"]; return o[i % o.length];
}

export function makeStub(args: { eyebrow: string; title: string; description: string; sections: { label: string; items: string[] }[] }): () => ReactNode {
  return function Page() { return <ModulePage {...args} />; };
}
