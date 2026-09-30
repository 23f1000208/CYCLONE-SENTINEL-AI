"use client";

import React, { useState } from "react";
import { CheckCircle2, XCircle, AlertTriangle, ShieldCheck, FileCheck, ExternalLink } from "lucide-react";

interface HumanApprovalDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  advisory: any;
  onActionComplete: () => void;
}

export default function HumanApprovalDrawer({
  isOpen,
  onClose,
  advisory,
  onActionComplete,
}: HumanApprovalDrawerProps) {
  const [notes, setNotes] = useState("Authorized by Incident Commander after route & shelter capacity verification.");
  const [isProcessing, setIsProcessing] = useState(false);
  const [showEvidence, setShowEvidence] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);

  if (!isOpen || !advisory) return null;

  const handleAction = async (action: "approve" | "reject") => {
    setIsProcessing(true);
    try {
      const res = await fetch(`/api/v1/advisories/${advisory.id}/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: action.toUpperCase(),
          decision_notes: notes,
        }),
      });
      const data = await res.json();
      setAuditResult(data);
      setTimeout(() => {
        onActionComplete();
        onClose();
      }, 1800);
    } catch (err) {
      console.error("Approval error", err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-[#0f172a] border border-slate-700 rounded-xl max-w-2xl w-full p-6 shadow-2xl font-mono text-xs flex flex-col space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-amber-400" />
            <span className="font-bold text-sm text-slate-100 uppercase tracking-wider">
              Human-in-the-Loop Advisory Review
            </span>
          </div>
          <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">
            STATE: {advisory.status || "DRAFT"}
          </span>
        </div>

        {/* Advisory Content Card */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="text-cyan-400 font-bold text-sm">{advisory.title}</div>
          <div className="text-slate-300 font-semibold">{advisory.headline}</div>
          <div className="text-slate-400 leading-relaxed font-sans text-xs bg-slate-950/60 p-3 rounded border border-slate-800/80">
            {advisory.advisory_text}
          </div>
          <div className="text-[10px] text-amber-500/90 pt-1">
            ⚠️ Disclaimer: {advisory.disclaimer}
          </div>
        </div>

        {/* Evidence Accordion Button */}
        <div>
          <button
            onClick={() => setShowEvidence(!showEvidence)}
            className="text-[11px] text-cyan-400 hover:text-cyan-300 flex items-center space-x-1 font-semibold"
          >
            <span>{showEvidence ? "[-] HIDE UNDERLYING EVIDENCE" : "[+] VIEW STRUCTURED EVIDENCE"}</span>
          </button>
          {showEvidence && (
            <div className="mt-2 p-3 bg-slate-950 rounded border border-slate-800 text-[10px] text-slate-300 space-y-1">
              <div>• Cyclone Wind Speed: 140 km/h (Very Severe Cyclonic Storm)</div>
              <div>• Modeled Peak Storm Surge: 2.5m (Paradeep - Astaranga sector)</div>
              <div>• Impacted Facilities: 3 hospitals at flood risk (H-103, H-105, H-107)</div>
              <div>• Flooded Corridors: 14 segments of Coastal Link Highway impassable</div>
              <div>• Safe Evacuation Hubs: Grand Road (S-201) & Gop Inland Refuge (S-208) verified</div>
            </div>
          )}
        </div>

        {/* Commander Decision Notes */}
        <div>
          <label className="text-slate-400 font-bold mb-1 block">OPERATIONAL DECISION NOTES:</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200 text-xs focus:outline-none focus:border-cyan-500 font-mono"
            rows={2}
          />
        </div>

        {/* Audit Status Result */}
        {auditResult && (
          <div className="p-2.5 bg-emerald-950/80 border border-emerald-700 rounded text-emerald-300 text-[11px] flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Advisory {auditResult.status}! Recorded in Audit Trail.</span>
            </div>
            <span className="font-mono text-[9px] text-emerald-400">
              HASH: {auditResult.audit_checksum ? auditResult.audit_checksum.substring(0, 16) : ""}...
            </span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3 pt-3 border-t border-slate-800">
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded text-slate-400 hover:text-slate-200 text-xs transition"
          >
            CANCEL
          </button>
          <button
            onClick={() => handleAction("reject")}
            disabled={isProcessing}
            className="px-4 py-2 rounded bg-red-950 hover:bg-red-900 text-red-300 border border-red-800 font-bold text-xs transition flex items-center space-x-1.5"
          >
            <XCircle className="w-4 h-4" />
            <span>REJECT ADVISORY</span>
          </button>
          <button
            onClick={() => handleAction("approve")}
            disabled={isProcessing}
            className="px-5 py-2 rounded bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs transition flex items-center space-x-1.5 shadow-lg"
          >
            <CheckCircle2 className="w-4 h-4 text-slate-950" />
            <span>APPROVE & DISSEMINATE</span>
          </button>
        </div>
      </div>
    </div>
  );
}
