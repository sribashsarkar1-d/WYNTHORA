import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/data-sources")({
  head: () => ({ meta: [{ title: "Data Sources — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Infrastructure · Data"
      title="Data Source Management"
      description="Global ingestion: institutional, scientific, financial, satellite, and news feeds."
      sections={[
        { label: "Sources", items: ["World Bank","IMF","UN","NOAA","NASA","GDELT","News APIs","Financial APIs","Trade APIs","Satellite APIs"] },
        { label: "Operations", items: ["API Keys","Health Monitoring","Refresh Data","ETL Jobs","Sync Status","Scheduler"] },
      ]}
    />
  ),
});
