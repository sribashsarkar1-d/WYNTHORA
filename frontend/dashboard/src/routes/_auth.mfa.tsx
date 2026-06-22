import { createFileRoute, Link } from "@tanstack/react-router";
import { ShieldCheck } from "lucide-react";
export const Route = createFileRoute("/_auth/mfa")({ component: Mfa });
function Mfa() {
  return (
    <div>
      <div className="mb-6 grid h-12 w-12 place-items-center rounded-xl bg-gradient-to-br from-cyan/20 to-purple/20 border border-cyan/30"><ShieldCheck className="h-6 w-6 text-cyan" /></div>
      <h1 className="font-display text-3xl font-bold">Multi-factor verification</h1>
      <p className="mt-2 text-sm text-muted-foreground">Enter the 6-digit code from your authenticator, or tap your hardware key.</p>
      <div className="mt-8 flex justify-center gap-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <input key={i} maxLength={1} defaultValue={["8","4","2","9","1","7"][i]} className="glass h-14 w-12 rounded-lg border border-border text-center font-mono text-2xl focus:border-cyan/50 focus:outline-none" />
        ))}
      </div>
      <Link to="/app/dashboard" className="mt-8 block w-full rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-center text-sm font-semibold text-background">Verify & enter console</Link>
      <button className="glass mt-3 flex w-full items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm">Use YubiKey instead</button>
      <p className="mt-8 text-center text-xs text-muted-foreground">Didn't receive a code? <a className="text-cyan hover:underline">Resend</a></p>
    </div>
  );
}
