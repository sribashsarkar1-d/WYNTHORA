import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/infrastructure")({
  head: () => ({ meta: [{ title: "Infrastructure Monitoring — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Infrastructure · Ops"
      title="Infrastructure Monitoring"
      description="Hardware, orchestration, streaming, and observability stack."
      sections={[
        { label: "Compute", items: ["Servers","Docker","Kubernetes","GPU Cluster","Ray Cluster"] },
        { label: "Streaming & Obs", items: ["Kafka","Airflow","Redis","Prometheus","Grafana"] },
        { label: "Edge", items: ["Storage","Network","Latency"] },
      ]}
    />
  ),
});
