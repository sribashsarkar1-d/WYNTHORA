import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/activity")({
  head: () => ({ meta: [{ title: "Activity Center — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Command · Activity"
      title="Activity Center"
      description="Unified timeline across system, users, audit, simulations, and agents."
      sections={[
        { label: "Timelines", items: ["System Timeline","User Timeline","Audit Timeline","Simulation Timeline","Agent Timeline"] },
        { label: "Tools", items: ["Replay","Bookmark","Annotate","Export Trace"] },
      ]}
    />
  ),
});
