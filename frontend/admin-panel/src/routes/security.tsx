import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/security")({
  head: () => ({ meta: [{ title: "Security Center — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Infrastructure · Security"
      title="Security Center"
      description="Zero-trust posture, identity, encryption, intrusion detection, and audit."
      sections={[
        { label: "Audit & Detection", items: ["Audit Logs","Access Logs","Threat Detection","Intrusion Detection","Security Score"] },
        { label: "Identity & Crypto", items: ["MFA","SSO","OAuth","API Security","Encryption","Firewall","Device Management"] },
      ]}
    />
  ),
});
