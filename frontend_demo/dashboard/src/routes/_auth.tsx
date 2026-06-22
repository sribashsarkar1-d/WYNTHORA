import { createFileRoute, Link, Outlet } from "@tanstack/react-router";
import { Globe2 } from "lucide-react";
import { Globe } from "@/components/wynthora";

export const Route = createFileRoute("/_auth")({ component: AuthLayout });

function AuthLayout() {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative hidden overflow-hidden lg:block" style={{ background: "var(--gradient-hero)" }}>
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="relative flex h-full flex-col justify-between p-12">
          <Link to="/" className="flex items-center gap-2">
            <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-cyan to-purple"><Globe2 className="h-5 w-5 text-background" /></div>
            <span className="text-lg font-bold tracking-[0.2em]">WYNTHORA</span>
          </Link>
          <div className="grid place-items-center"><Globe size={380} /></div>
          <div className="space-y-2">
            <blockquote className="text-xl font-light leading-snug">"The most consequential decisions of the next century will be made with WYNTHORA in the loop."</blockquote>
            <div className="text-xs uppercase tracking-widest text-muted-foreground">— The Economist Intelligence Review</div>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-center p-6 lg:p-12">
        <div className="w-full max-w-md"><Outlet /></div>
      </div>
    </div>
  );
}
