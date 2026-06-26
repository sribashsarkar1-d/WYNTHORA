import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/databases")({
  head: () => ({ meta: [{ title: "Database Management — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Infrastructure · Storage"
      title="Database Management"
      description="Operational and analytical stores powering the simulation fabric."
      sections={[
        { label: "Engines", items: ["PostgreSQL","Redis","ClickHouse","Snowflake"] },
        { label: "Operations", items: ["Database Health","Backup","Restore","Migration","Performance"] },
      ]}
    />
  ),
});
