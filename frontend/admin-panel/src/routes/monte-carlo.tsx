import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/monte-carlo")({
  head: () => ({ meta: [{ title: "Monte Carlo Engine — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="AI Core · Stochastic"
      title="Monte Carlo Engine"
      description="Massive-iteration stochastic simulation with full sensitivity and risk distribution analytics."
      sections={[
        { label: "Runs", items: ["Iterations","Probability Distribution","Confidence Interval","Simulation Results"] },
        { label: "Analysis", items: ["Sensitivity Analysis","Risk Distribution","Variance Decomposition","Scenario Stress"] },
      ]}
    />
  ),
});
