import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { ShieldAlert, Activity, FileText, CheckCircle2, History, Radio } from "lucide-react";

export const metadata: Metadata = {
  title: "CYCLONE SENTINEL AI — Emergency Command Center",
  description: "Cyclone Impact & Infrastructure Vulnerability Forecaster — Anticipatory Action Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#090d16] text-slate-100 min-h-screen flex flex-col">
        {/* Top Emergency Operations Header */}
        <header className="border-b border-slate-800 bg-[#0d1322] px-6 py-3 flex items-center justify-between sticky top-0 z-50 shadow-md">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-red-950/60 border border-red-500/50 rounded-lg text-red-400 flex items-center justify-center">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-wider text-slate-50">CYCLONE SENTINEL AI</span>
                <span className="text-xs px-2 py-0.5 rounded font-mono bg-cyan-950 text-cyan-400 border border-cyan-800">
                  TRACK 5
                </span>
                <span className="flex items-center space-x-1.5 text-xs text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                  <span>ACTIVE MONITORING</span>
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono">
                Predict the Impact. Protect the Infrastructure. Act Before Landfall.
              </p>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="flex items-center space-x-1 bg-slate-900/80 p-1 border border-slate-800 rounded-lg">
            <Link
              href="/"
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded text-slate-200 hover:bg-slate-800 hover:text-cyan-400 transition"
            >
              <Activity className="w-4 h-4" />
              <span>Command Center</span>
            </Link>
            <Link
              href="/approvals"
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded text-slate-300 hover:bg-slate-800 hover:text-cyan-400 transition"
            >
              <CheckCircle2 className="w-4 h-4 text-amber-400" />
              <span>Human Approvals</span>
            </Link>
            <Link
              href="/audit"
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded text-slate-300 hover:bg-slate-800 hover:text-cyan-400 transition"
            >
              <History className="w-4 h-4 text-indigo-400" />
              <span>Audit Trail</span>
            </Link>
          </nav>

          {/* System Provenance Badge */}
          <div className="hidden lg:flex items-center space-x-3 text-right">
            <div>
              <div className="text-xs font-mono text-slate-300">CURRENT TARGET: <span className="text-amber-400 font-bold">CYCLONE DEMO-01</span></div>
              <div className="text-[10px] font-mono text-slate-500">Bay of Bengal Sector 4 • Zero-LLM Arithmetic Engine</div>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 flex flex-col">{children}</main>
      </body>
    </html>
  );
}
