import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/billing")({
  head: () => ({ meta: [{ title: "Billing — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Operations · Billing"
      title="Billing & Subscription"
      description="Enterprise contracts, plans, invoices, and revenue intelligence."
      sections={[
        { label: "Commercial", items: ["Plans","Enterprise Contracts","Coupons","Taxes"] },
        { label: "Financial", items: ["Invoices","Transactions","Usage Billing","Revenue Analytics"] },
      ]}
    />
  ),
});
