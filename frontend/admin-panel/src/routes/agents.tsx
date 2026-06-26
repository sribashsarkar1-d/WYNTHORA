import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/agents")({
  head: () => ({ meta: [{ title: "Multi-Agent Management — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="AI Core · Agents"
      title="Multi-Agent Management"
      description="Orchestrate domain-specialized AI agents that drive the global simulation fabric."
      sections={[
        { label: "Agent Domains", items: ["Economic Agents","Political Agents","Climate Agents","Business Agents","Military Agents","Health Agents","Trade Agents","Technology Agents","Population Agents"] },
        { label: "Runtime Controls", items: ["Start","Stop","Restart","Clone","Logs","Performance","Resource Usage"] },
      ]}
    />
  ),
});
