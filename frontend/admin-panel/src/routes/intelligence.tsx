import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/intelligence")({
  head: () => ({ meta: [{ title: "Intelligence Center — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Command · Intel"
      title="Intelligence Center"
      description="Cross-domain threat, risk, and signal intelligence — live and AI-augmented."
      sections={[
        { label: "Monitoring", items: ["Threat Monitoring","Risk Monitoring","Real Time Alerts"] },
        { label: "Domains", items: ["Economic Intelligence","Political Intelligence","Climate Intelligence","News Intelligence","AI Insights"] },
      ]}
    />
  ),
});
