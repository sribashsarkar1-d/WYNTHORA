import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/simulations")({
  head: () => ({ meta: [{ title: "Simulations — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="AI Core · Simulations"
      title="Simulation Management"
      description="Author, queue, run, and inspect multi-domain simulations across the digital twin."
      sections={[
        { label: "Lifecycle", items: ["Create Simulation","Stop Simulation","Pause","Resume","Queue","History"] },
        { label: "Inspection", items: ["Scenario Templates","Simulation Graph","Simulation Timeline","Live Monitoring","Simulation Logs"] },
      ]}
    />
  ),
});
