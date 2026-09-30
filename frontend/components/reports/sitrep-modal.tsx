"use client";

import React from "react";
import { FileText, Printer, CheckCircle, ShieldAlert, Download } from "lucide-react";

interface SitRepModalProps {
  isOpen: boolean;
  onClose: () => void;
  cyclone: any;
  risk: any;
}

export default function SitRepModal({ isOpen, onClose, cyclone, risk }: SitRepModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-[#0f172a] border border-slate-700 rounded-xl max-w-3xl w-full p-6 shadow-2xl font-mono text-xs flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <span className="font-bold text-sm text-slate-100 uppercase tracking-wider">
              CYCLONE SENTINEL SITUATION REPORT (SITREP-01)
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white px-2 py-1 font-bold">
            ✕
          </button>
        </div>

        {/* Scrollable Report Content */}
        <div className="flex-1 overflow-y-auto my-4 space-y-4 pr-2 font-sans text-xs text-slate-200 leading-relaxed">
          {/* Executive Summary */}
          <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800">
            <div className="font-bold text-cyan-400 font-mono mb-1 text-sm">1. EXECUTIVE SUMMARY</div>
            <p>
              Cyclone DEMO-01 is tracking northwest across the Bay of Bengal and is anticipated to make landfall
              along the central Odisha coastline within 6 to 9 hours. Deterministic multi-hazard risk modeling evaluates
              the regional hazard level at <strong>HIGH (0.76)</strong>. Elevated storm surge (2.5m) and surface runoff (180mm)
              threaten critical infrastructure, rendering 3 hospitals at high inundation risk and cutting 14 road segments.
            </p>
          </div>

          {/* Meteorological Status */}
          <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800 font-mono text-[11px]">
            <div className="font-bold text-cyan-400 mb-1 text-xs">2. CURRENT CYCLONE OBSERVATION</div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-slate-300">
              <div>Sustained Wind: <span className="text-white font-bold">140 km/h</span></div>
              <div>Central Pressure: <span className="text-white font-bold">968 hPa</span></div>
              <div>Movement: <span className="text-white font-bold">NW at 18 km/h</span></div>
              <div>Position: <span className="text-white font-bold">19.45°N, 86.80°E</span></div>
            </div>
          </div>

          {/* Infrastructure Impact */}
          <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800">
            <div className="font-bold text-cyan-400 font-mono mb-1 text-sm">3. INFRASTRUCTURE & FACILITY EXPOSURE</div>
            <ul className="list-disc list-inside space-y-1 text-slate-300">
              <li><strong>Healthcare</strong>: 3 of 12 regional hospitals face severe access disruption due to low elevation and access road submergence (H-103 Konark, H-105 Astaranga, H-107 Ersama).</li>
              <li><strong>Transport Corridors</strong>: 14 coastal highway segments are modeled as impassable (&gt;30cm flood depth).</li>
              <li><strong>Power Grid</strong>: 4 coastal 33kV substations are within the modeled 2.5m storm surge inundation contour.</li>
            </ul>
          </div>

          {/* Population Exposure */}
          <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800">
            <div className="font-bold text-cyan-400 font-mono mb-1 text-sm">4. POPULATION EXPOSURE & SHELTER DEMAND</div>
            <p className="text-slate-300">
              Approximately <strong>248,000 residents</strong> reside within the high-hazard zone.
              Estimated emergency shelter demand is <strong>54,500 slots</strong>. The 8 regional multi-purpose cyclone
              shelters provide an aggregate safe capacity of 62,500, indicating an overall capacity surplus (+8,000 slots)
              provided evacuees are guided toward inland high-perch refuges (S-201 and S-208).
            </p>
          </div>

          {/* Provenance & Disclaimer */}
          <div className="bg-red-950/20 border border-red-900/60 p-3 rounded text-[11px] text-red-300">
            <strong>Scientific & Statutory Disclaimer</strong>: This situation report is compiled by the CYCLONE SENTINEL AI
            decision-support prototype using deterministic SLOSH and hydrologic models. It does NOT constitute a statutory
            government warning. Operational evacuation orders must be issued by authorized disaster management officials.
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-slate-800 pt-3">
          <span className="text-[10px] text-slate-500 font-mono">
            Generated: {new Date().toISOString()} • Model: Sentinel-Risk-v1.4
          </span>
          <div className="flex space-x-2">
            <button
              onClick={() => window.print()}
              className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition flex items-center space-x-1"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>PRINT REPORT</span>
            </button>
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold transition"
            >
              CLOSE
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
