"use client";

import React, { useState, useEffect } from "react";
import { History, Shield, Check, Key } from "lucide-react";

export default function AuditPage() {
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    fetch("/api/v1/audit")
      .then((res) => res.json())
      .then((data) => setLogs(data))
      .catch((e) => console.warn(e));
  }, []);

  return (
    <div className="flex-1 p-6 bg-[#080d16] font-mono text-xs max-w-6xl mx-auto w-full space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <History className="w-6 h-6 text-indigo-400" />
            <span>TAMPER-EVIDENT AUDIT TRAIL LOG</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Section 40 Compliance: Immutable records of all simulations, recommendations, approvals, and checksums.
          </p>
        </div>
        <span className="px-3 py-1 rounded bg-indigo-950/80 text-indigo-400 border border-indigo-800 font-bold flex items-center space-x-1.5">
          <Key className="w-3.5 h-3.5" />
          <span>SHA-256 HASH CHAINING</span>
        </span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-[11px]">
              <th className="p-3">TIMESTAMP</th>
              <th className="p-3">EVENT TYPE</th>
              <th className="p-3">ACTOR</th>
              <th className="p-3">ACTION</th>
              <th className="p-3">SHA-256 CHECKSUM</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-[11px] text-slate-300">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-slate-800/40 transition">
                <td className="p-3 text-slate-400 whitespace-nowrap">
                  {new Date(log.timestamp).toLocaleString()}
                </td>
                <td className="p-3">
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-cyan-400 border border-slate-700 text-[10px]">
                    {log.event_type}
                  </span>
                </td>
                <td className="p-3 font-semibold text-white">{log.actor}</td>
                <td className="p-3 text-amber-400">{log.action}</td>
                <td className="p-3 font-mono text-emerald-400 text-[10px]">
                  {log.checksum ? log.checksum.substring(0, 24) + "..." : "SYSTEM_SEEDED"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
