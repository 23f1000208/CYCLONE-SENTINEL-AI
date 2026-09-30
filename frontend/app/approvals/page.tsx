"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, CheckCircle2, XCircle, AlertTriangle, FileText } from "lucide-react";

export default function ApprovalsPage() {
  const [advisories, setAdvisories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAdvisories = async () => {
    try {
      const res = await fetch("/api/v1/advisories");
      if (res.ok) setAdvisories(await res.json());
    } catch (e) {
      console.warn("Offline advisories fallback", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdvisories();
  }, []);

  const handleAction = async (id: string, action: "approve" | "reject") => {
    try {
      await fetch(`/api/v1/advisories/${id}/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: action.toUpperCase() }),
      });
      fetchAdvisories();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 p-6 bg-[#080d16] font-mono text-xs max-w-6xl mx-auto w-full space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <ShieldCheck className="w-6 h-6 text-amber-400" />
            <span>HUMAN-IN-THE-LOOP APPROVAL PORTAL</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Section 21 Compliance: Authorized Disaster Manager review required before advisory dissemination.
          </p>
        </div>
        <span className="px-3 py-1 rounded bg-amber-950/80 text-amber-400 border border-amber-800 font-bold">
          ROLE: DISASTER_MANAGER
        </span>
      </div>

      <div className="space-y-4">
        {advisories.map((a) => (
          <div key={a.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs px-2 py-0.5 rounded font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
                {a.id} • {a.risk_level} ALERT
              </span>
              <span
                className={`text-xs px-2.5 py-0.5 rounded font-bold ${
                  a.status === "APPROVED"
                    ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                    : a.status === "REJECTED"
                    ? "bg-red-950 text-red-400 border border-red-800"
                    : "bg-amber-950 text-amber-400 border border-amber-800"
                }`}
              >
                STATUS: {a.status}
              </span>
            </div>

            <h2 className="text-sm font-bold text-slate-100">{a.title}</h2>
            <div className="text-slate-300 font-semibold">{a.headline}</div>
            <p className="text-slate-400 font-sans leading-relaxed bg-slate-950 p-3 rounded border border-slate-800">
              {a.advisory_text}
            </p>

            <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
              <span className="text-[10px] text-slate-500">
                Created: {new Date(a.created_at).toLocaleString()} • {a.disclaimer}
              </span>

              {a.status === "DRAFT" && (
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleAction(a.id, "reject")}
                    className="px-3 py-1.5 rounded bg-red-950 hover:bg-red-900 text-red-300 border border-red-800 transition font-bold"
                  >
                    REJECT
                  </button>
                  <button
                    onClick={() => handleAction(a.id, "approve")}
                    className="px-4 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold transition shadow"
                  >
                    APPROVE & ISSUE
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
