import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { AppSidebar } from "../components/shell/AppSidebar";
import { Topbar } from "../components/shell/Topbar";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="max-w-md text-center">
        <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary mb-3">ERROR · 404</div>
        <h1 className="font-display text-6xl font-bold gradient-text">Lost in the simulation</h1>
        <p className="mt-3 text-sm text-muted-foreground">This route does not exist in the current timeline.</p>
        <Link to="/" className="mt-6 inline-flex items-center justify-center rounded-md bg-[var(--gradient-aurora)] px-4 py-2 text-sm font-semibold text-primary-foreground glow-cyan">
          Return to Command
        </Link>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => { reportLovableError(error, { boundary: "tanstack_root_error_component" }); }, [error]);
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="max-w-md text-center rounded-xl glass p-6">
        <h1 className="font-display text-xl font-semibold">Subsystem failure</h1>
        <p className="mt-2 text-sm text-muted-foreground">An unhandled fault occurred. Try reloading the panel.</p>
        <div className="mt-5 flex justify-center gap-2">
          <button onClick={() => { router.invalidate(); reset(); }} className="rounded-md bg-[var(--gradient-aurora)] px-4 py-2 text-sm font-semibold text-primary-foreground">Try again</button>
          <a href="/" className="rounded-md border border-border px-4 py-2 text-sm">Home</a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "WYNTHORA — AI World Simulation Engine" },
      { name: "description", content: "Enterprise command center for the WYNTHORA AI-powered world simulation engine." },
      { name: "author", content: "WYNTHORA" },
      { property: "og:title", content: "WYNTHORA — AI World Simulation Engine" },
      { property: "og:description", content: "Enterprise command center for the WYNTHORA AI-powered world simulation engine." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
    links: [{ rel: "stylesheet", href: appCss }],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head><HeadContent /></head>
      <body>{children}<Scripts /></body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <Topbar />
          <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">
            <Outlet />
          </main>
        </div>
      </div>
    </QueryClientProvider>
  );
}
