import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/reports")({
  head: () => ({ meta: [{ title: "Reports — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Operations · Reports"
      title="Reports"
      description="Executive briefings, simulation deliverables, and recurring exports."
      sections={[
        { label: "Reports", items: ["Executive Reports","Simulation Reports","Financial Reports","Climate Reports","Scheduled Reports"] },
        { label: "Export", items: ["Export PDF","Export Excel","Export CSV","API Export"] },
      ]}
    />
  ),
});
