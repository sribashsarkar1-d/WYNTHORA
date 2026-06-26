import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/models")({
  head: () => ({ meta: [{ title: "AI Model Management — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="AI Core · Models"
      title="AI Model Management"
      description="Registry, training, deployment and lifecycle for every foundation, reasoning, and domain model."
      sections={[
        { label: "Registry & Versions", items: ["Model Registry","Version Control","Deploy Model","Rollback","Prompt Library"] },
        { label: "Training & Metrics", items: ["Training Status","Accuracy","Loss Curves","Performance Metrics","GPU Allocation"] },
        { label: "Model Families", items: ["LLM Management","Embedding Models","Vision Models","Reasoning Models"] },
      ]}
    />
  ),
});
