"use client";

import React from "react";
import { Wind, CloudRain, Waves, Users, Building2, Hospital } from "lucide-react";

interface KpiData {
  windSpeedKmh: number;
  pressureHpa: number;
  rainfallMm: number;
  stormSurgeM: number;
  exposedPopulation: number;
  exposedInfraCount: number;
  atRiskHospitals: number;
  riskCategory: string;
}

export default function KpiBar({ data }: { data: KpiData }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 px-6 py-4 bg-[#0c1220] border-b border-slate-800">
      {/* 1. Cyclone Intensity */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>CYCLONE INTENSITY</span>
          <Wind className="w-4 h-4 text-cyan-400" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{data.windSpeedKmh}</span>
          <span className="text-xs text-slate-400 font-mono">km/h</span>
        </div>
        <div className="text-[11px] text-slate-400 font-mono mt-0.5">
          {data.pressureHpa} hPa • Very Severe
        </div>
      </div>

      {/* 2. Rainfall */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>PRECIPITATION</span>
          <CloudRain className="w-4 h-4 text-blue-400" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{data.rainfallMm}</span>
          <span className="text-xs text-slate-400 font-mono">mm</span>
        </div>
        <div className="text-[11px] text-blue-400 font-mono mt-0.5">
          Extreme Surface Runoff
        </div>
      </div>

      {/* 3. Storm Surge */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>STORM SURGE</span>
          <Waves className="w-4 h-4 text-indigo-400" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{data.stormSurgeM}</span>
          <span className="text-xs text-slate-400 font-mono">m</span>
        </div>
        <div className="text-[11px] text-indigo-400 font-mono mt-0.5">
          Peak Coastal Inundation
        </div>
      </div>

      {/* 4. Population Exposed */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>POPULATION EXPOSED</span>
          <Users className="w-4 h-4 text-amber-400" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-amber-400 tracking-tight">
            {data.exposedPopulation.toLocaleString()}
          </span>
        </div>
        <div className="text-[11px] text-slate-400 font-mono mt-0.5">
          Across 5 Coastal Zones
        </div>
      </div>

      {/* 5. Infrastructure at Risk */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>INFRASTRUCTURE</span>
          <Building2 className="w-4 h-4 text-orange-400" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{data.exposedInfraCount}</span>
          <span className="text-xs text-slate-400 font-mono">assets</span>
        </div>
        <div className="text-[11px] text-orange-400 font-mono mt-0.5">
          Roads & Substations Flooded
        </div>
      </div>

      {/* 6. Hospitals at Risk */}
      <div className="bg-slate-900/90 border border-red-950/60 rounded-lg p-3 relative overflow-hidden bg-gradient-to-br from-red-950/20 to-slate-900">
        <div className="flex items-center justify-between text-xs text-red-400 font-mono font-bold">
          <span>HOSPITALS IMPAIRED</span>
          <Hospital className="w-4 h-4 text-red-400 animate-pulse" />
        </div>
        <div className="mt-1 flex items-baseline space-x-1.5">
          <span className="text-2xl font-bold text-red-400 tracking-tight">{data.atRiskHospitals}</span>
          <span className="text-xs text-slate-400 font-mono">of 12</span>
        </div>
        <div className="text-[11px] text-red-300 font-mono mt-0.5 font-semibold">
          High Flood Exposure
        </div>
      </div>
    </div>
  );
}
