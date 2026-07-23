import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { Fingerprint, KeyRound, Mail, Loader2 } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/_auth/login")({ component: Login });

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Mock API call
    setTimeout(() => {
      setIsLoading(false);
      navigate({ to: "/app/dashboard" });
    }, 1000);
  };

  return (
    <div>
      <h1 className="font-display text-3xl font-bold">Sign in to the engine</h1>
      <p className="mt-2 text-sm text-muted-foreground">Authenticated, audited, end-to-end encrypted.</p>
      <form onSubmit={handleSubmit} className="mt-8 space-y-4">
        <Field icon={<Mail className="h-4 w-4" />} label="Work email" type="email" placeholder="analyst@institution.gov" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <Field icon={<KeyRound className="h-4 w-4" />} label="Password" type="password" placeholder="••••••••••••" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <div className="flex items-center justify-between text-xs">
          <label className="flex items-center gap-2 text-muted-foreground"><input type="checkbox" className="accent-cyan" /> Remember this device</label>
          <Link to="/forgot-password" className="text-cyan hover:underline">Forgot password?</Link>
        </div>
        <button type="submit" disabled={isLoading} className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-sm font-semibold text-background glow-cyan disabled:opacity-70 transition">
          {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
          Continue
        </button>
      </form>
      <div className="my-6 flex items-center gap-3 text-xs text-muted-foreground"><div className="h-px flex-1 bg-border" />or<div className="h-px flex-1 bg-border" /></div>
      <div className="space-y-2">
        <button className="glass flex w-full items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm"><Fingerprint className="h-4 w-4 text-cyan" /> Continue with SSO / SAML</button>
        <button className="glass flex w-full items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm">Continue with Okta</button>
        <button className="glass flex w-full items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm">Continue with Microsoft Entra</button>
      </div>
      <p className="mt-8 text-center text-xs text-muted-foreground">No account? <Link to="/register" className="text-cyan hover:underline">Request access</Link></p>
    </div>
  );
}

export function Field({ icon, label, ...p }: { icon?: React.ReactNode; label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="block">
      <div className="mb-1.5 text-xs font-medium uppercase tracking-wider text-muted-foreground">{label}</div>
      <div className="glass flex items-center gap-2 rounded-lg border border-border px-3 focus-within:border-cyan/50">
        {icon && <span className="text-muted-foreground">{icon}</span>}
        <input {...p} className="h-10 w-full bg-transparent text-sm focus:outline-none placeholder:text-muted-foreground" />
      </div>
    </label>
  );
}
