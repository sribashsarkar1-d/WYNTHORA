import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/digital-twin")({
  head: () => ({ meta: [{ title: "Digital Twin Earth — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="AI Core · Twin"
      title="Digital Twin Earth"
      description="Layered 3D model of the planet — economy, climate, conflict, satellites, infrastructure."
      sections={[
        { label: "Viewport", items: ["3D Earth","Layers","Satellite Layers"] },
        { label: "Layers", items: ["Countries","Population","Economy","Climate","Trade Routes","Conflict Zones","Infrastructure"] },
      ]}
    />
  ),
});
