import { createFileRoute } from "@tanstack/react-router";
import { Dashboard } from "@/components/dashboard/Dashboard";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Command Dashboard — WYNTHORA" },
      { name: "description", content: "Executive command dashboard for the WYNTHORA simulation engine." },
    ],
  }),
  component: Dashboard,
});
