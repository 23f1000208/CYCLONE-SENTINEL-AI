"use client";

import React, { useState } from "react";
import { Layers, Eye, EyeOff, Navigation, AlertTriangle, ShieldCheck } from "lucide-react";

interface CommandMapProps {
  cycloneData: any;
  hospitals: any[];
  shelters: any[];
  roads: any[];
  power: any[];
  surgeData: any;
}

export default function CommandMap({
  cycloneData,
  hospitals,
  shelters,
  roads,
  power,
  surgeData,
}: CommandMapProps) {
  // 10 Layer toggle states
  const [layers, setLayers] = useState({
    track: true,
    cone: true,
    windField: true,
    rainfall: true,
    stormSurge: true,
    floodRisk: true,
    roads: true,
    hospitals: true,
    shelters: true,
    power: true,
  });

  const [selectedAsset, setSelectedAsset] = useState<any>(null);

  const toggleLayer = (layerKey: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [layerKey]: !prev[layerKey] }));
  };

  // Map coordinate transformation helper
  // Bay of Bengal Sector 4: Lat 19.4 to 20.6 (1.2 deg), Lon 85.4 to 87.0 (1.6 deg)
  const minLat = 19.3, maxLat = 20.7;
  const minLon = 85.3, maxLon = 87.1;

  const toMapCoords = (lat: number, lon: number) => {
    const x = ((lon - minLon) / (maxLon - minLon)) * 100;
    const y = ((maxLat - lat) / (maxLat - minLat)) * 100;
    return { x: Math.max(2, Math.min(98, x)), y: Math.max(2, Math.min(98, y)) };
  };

  const cyclonePos = cycloneData?.current_location
    ? toMapCoords(cycloneData.current_location.lat, cycloneData.current_location.lon)
    : { x: 75, y: 70 };

  return (
    <div className="relative w-full h-[540px] bg-[#070b12] rounded-xl border border-slate-800 overflow-hidden flex flex-col shadow-2xl">
      {/* Top Map Header Controls */}
      <div className="absolute top-3 left-3 z-30 flex items-center space-x-2 bg-slate-900/90 backdrop-blur-md border border-slate-800 px-3 py-1.5 rounded-lg shadow-lg">
        <Navigation className="w-4 h-4 text-cyan-400" />
        <span className="text-xs font-mono text-slate-200 font-semibold">GEOSPATIAL COMMAND VIEW</span>
        <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800">
          BAY OF BENGAL
        </span>
      </div>

      {/* 10 Layer Controller Drawer (Top Right) */}
      <div className="absolute top-3 right-3 z-30 bg-slate-900/95 backdrop-blur-md border border-slate-800 rounded-lg p-2.5 shadow-xl max-w-xs text-xs font-mono">
        <div className="flex items-center space-x-1.5 pb-2 mb-2 border-b border-slate-800 text-slate-300 font-bold">
          <Layers className="w-3.5 h-3.5 text-cyan-400" />
          <span>GIS MAP LAYERS (10)</span>
        </div>
        <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 text-[11px]">
          {Object.entries({
            track: "Cyclone Track",
            cone: "Forecast Cone",
            windField: "Wind Field",
            rainfall: "Rainfall",
            stormSurge: "Storm Surge",
            floodRisk: "Flood Zones",
            roads: "Roads (45)",
            hospitals: "Hospitals (12)",
            shelters: "Shelters (8)",
            power: "Power (15)",
          }).map(([key, label]) => {
            const active = layers[key as keyof typeof layers];
            return (
              <button
                key={key}
                onClick={() => toggleLayer(key as keyof typeof layers)}
                className={`flex items-center space-x-1.5 px-1.5 py-0.5 rounded transition text-left ${
                  active
                    ? "text-slate-200 bg-slate-800/80 border border-slate-700 font-semibold"
                    : "text-slate-500 hover:text-slate-400"
                }`}
              >
                {active ? <Eye className="w-3 h-3 text-cyan-400" /> : <EyeOff className="w-3 h-3" />}
                <span className="truncate">{label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Interactive SVG Map Canvas */}
      <div className="relative flex-1 w-full h-full bg-[#080d17]">
        <svg className="w-full h-full select-none" viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs>
            {/* Ocean & Land Gradients */}
            <radialGradient id="surgeGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#0284c7" stopOpacity="0.05" />
            </radialGradient>
            <radialGradient id="windGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ef4444" stopOpacity="0.30" />
              <stop offset="70%" stopColor="#f59e0b" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
            </radialGradient>
            <linearGradient id="coneGradient" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#eab308" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#eab308" stopOpacity="0.05" />
            </linearGradient>
          </defs>

          {/* 1. Base Coastline & Ocean Representation */}
          {/* Inland Region (Left / Northwest) */}
          <path
            d="M 0,0 L 58,0 Q 64,30 68,55 Q 74,78 78,100 L 0,100 Z"
            fill="#111827"
            stroke="#1f293d"
            strokeWidth="0.4"
          />
          {/* Bay of Bengal Ocean (Right / Southeast) */}
          <path
            d="M 58,0 Q 64,30 68,55 Q 74,78 78,100 L 100,100 L 100,0 Z"
            fill="#091424"
          />
          {/* High Tide Coastline Boundary */}
          <path
            d="M 58,0 Q 64,30 68,55 Q 74,78 78,100"
            fill="none"
            stroke="#38bdf8"
            strokeWidth="0.6"
            strokeDasharray="2,1"
            opacity="0.7"
          />

          {/* 2. Storm Surge Inundation Swath */}
          {layers.stormSurge && (
            <polygon
              points="54,22 68,26 73,58 62,65 52,45"
              fill="url(#surgeGradient)"
              stroke="#0284c7"
              strokeWidth="0.5"
            />
          )}

          {/* 3. Surface Flood Risk Overlay */}
          {layers.floodRisk && (
            <g opacity="0.35">
              <ellipse cx="48" cy="42" rx="14" ry="9" fill="#2563eb" />
              <ellipse cx="58" cy="62" rx="12" ry="8" fill="#1d4ed8" />
            </g>
          )}

          {/* 4. Forecast Cone */}
          {layers.cone && (
            <polygon
              points="75,70 54,42 42,22 34,10 46,6 62,18 72,36 82,62"
              fill="url(#coneGradient)"
              stroke="#eab308"
              strokeWidth="0.3"
              strokeDasharray="1.5,1"
            />
          )}

          {/* 5. Wind Field Buffer (120km) */}
          {layers.windField && (
            <circle
              cx={cyclonePos.x}
              cy={cyclonePos.y}
              r="22"
              fill="url(#windGradient)"
              stroke="#ef4444"
              strokeWidth="0.4"
              strokeDasharray="1,1"
            />
          )}

          {/* 6. Cyclone Projected Track Line */}
          {layers.track && (
            <g>
              {/* Historical Track */}
              <polyline
                points="90,88 83,78 75,70"
                fill="none"
                stroke="#64748b"
                strokeWidth="0.8"
                strokeDasharray="1,1"
              />
              {/* Projected Track */}
              <polyline
                points="75,70 58,48 48,32 38,12"
                fill="none"
                stroke="#f97316"
                strokeWidth="1.0"
              />
              {/* Eye of Cyclone */}
              <circle cx={cyclonePos.x} cy={cyclonePos.y} r="2.2" fill="#ef4444" stroke="#ffffff" strokeWidth="0.5">
                <animate attributeName="r" values="2.0;2.6;2.0" dur="2s" repeatCount="indefinite" />
              </circle>
            </g>
          )}

          {/* 7. Road Network Segments */}
          {layers.roads &&
            roads.map((r, i) => {
              const start = toMapCoords(r.start_lat, r.start_lon);
              const end = toMapCoords(r.end_lat, r.end_lon);
              const isFlooded = r.passability !== "PASSABLE";
              return (
                <line
                  key={r.id || i}
                  x1={start.x}
                  y1={start.y}
                  x2={end.x}
                  y2={end.y}
                  stroke={isFlooded ? "#ef4444" : "#475569"}
                  strokeWidth={isFlooded ? "0.8" : "0.5"}
                  strokeDasharray={isFlooded ? "1,0.5" : "none"}
                  className="cursor-pointer hover:stroke-cyan-400"
                  onClick={() => setSelectedAsset({ type: "ROAD", data: r })}
                />
              );
            })}

          {/* 8. Power Infrastructure */}
          {layers.power &&
            power.map((p, i) => {
              const pos = toMapCoords(p.lat, p.lon);
              return (
                <circle
                  key={p.id || i}
                  cx={pos.x}
                  cy={pos.y}
                  r="1.0"
                  fill="#eab308"
                  stroke="#78350f"
                  strokeWidth="0.3"
                  className="cursor-pointer hover:r-2 transition"
                  onClick={() => setSelectedAsset({ type: "POWER", data: p })}
                />
              );
            })}

          {/* 9. Cyclone Shelters */}
          {layers.shelters &&
            shelters.map((s, i) => {
              const pos = toMapCoords(s.lat, s.lon);
              return (
                <polygon
                  key={s.id || i}
                  points={`${pos.x},${pos.y - 1.4} ${pos.x - 1.2},${pos.y + 1.2} ${pos.x + 1.2},${pos.y + 1.2}`}
                  fill="#10b981"
                  stroke="#ffffff"
                  strokeWidth="0.3"
                  className="cursor-pointer hover:opacity-80"
                  onClick={() => setSelectedAsset({ type: "SHELTER", data: s })}
                />
              );
            })}

          {/* 10. Hospitals */}
          {layers.hospitals &&
            hospitals.map((h, i) => {
              const pos = toMapCoords(h.lat, h.lon);
              const isImpaired = !h.is_accessible || h.inundation_risk >= 0.70;
              return (
                <g
                  key={h.id || i}
                  className="cursor-pointer"
                  onClick={() => setSelectedAsset({ type: "HOSPITAL", data: h })}
                >
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={isImpaired ? "1.8" : "1.4"}
                    fill={isImpaired ? "#dc2626" : "#0284c7"}
                    stroke="#ffffff"
                    strokeWidth="0.4"
                  />
                  {isImpaired && (
                    <circle cx={pos.x} cy={pos.y} r="3.2" fill="none" stroke="#ef4444" strokeWidth="0.3" opacity="0.8">
                      <animate attributeName="r" values="2.0;4.5" dur="1.8s" repeatCount="indefinite" />
                      <animate attributeName="opacity" values="0.9;0" dur="1.8s" repeatCount="indefinite" />
                    </circle>
                  )}
                </g>
              );
            })}
        </svg>

        {/* Selected Asset Inspection Card (Bottom Left Overlay) */}
        {selectedAsset && (
          <div className="absolute bottom-4 left-4 z-40 bg-slate-900/95 backdrop-blur-md border border-cyan-800 rounded-lg p-3 max-w-sm shadow-2xl text-xs font-mono">
            <div className="flex items-center justify-between border-b border-slate-800 pb-1.5 mb-2">
              <span className="font-bold text-cyan-400">
                {selectedAsset.type}: {selectedAsset.data.name || selectedAsset.data.id}
              </span>
              <button
                onClick={() => setSelectedAsset(null)}
                className="text-slate-400 hover:text-white px-1 font-bold"
              >
                ✕
              </button>
            </div>
            <div className="space-y-1 text-slate-300 text-[11px]">
              {selectedAsset.type === "HOSPITAL" && (
                <>
                  <div>Status: <span className={selectedAsset.data.is_accessible ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>
                    {selectedAsset.data.is_accessible ? "ACCESSIBLE" : "IMPAIRED / INACCESSIBLE"}
                  </span></div>
                  <div>Bed Capacity: {selectedAsset.data.bed_capacity} (ICU: {selectedAsset.data.icu_capacity})</div>
                  <div>Ground Elevation: {selectedAsset.data.elevation_m}m • Inundation Risk: {selectedAsset.data.inundation_risk}</div>
                  <div>Generator Backup: {selectedAsset.data.emergency_generator_hours}h</div>
                </>
              )}
              {selectedAsset.type === "SHELTER" && (
                <>
                  <div>Total Capacity: <span className="text-emerald-400 font-bold">{selectedAsset.data.total_capacity} persons</span></div>
                  <div>Current Occupancy: {selectedAsset.data.current_occupancy}</div>
                  <div>Medical Facility: {selectedAsset.data.medical_facility ? "Equipped" : "None"}</div>
                  <div>Elevation: {selectedAsset.data.elevation_m}m (Safe High-Perch)</div>
                </>
              )}
              {selectedAsset.type === "ROAD" && (
                <>
                  <div>Status: <span className={selectedAsset.data.passability === "PASSABLE" ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>
                    {selectedAsset.data.passability}
                  </span></div>
                  <div>Flood Depth: {selectedAsset.data.flood_depth_cm} cm</div>
                  <div>Elevation: {selectedAsset.data.elevation_m}m • Coast Dist: {selectedAsset.data.distance_to_coast_km}km</div>
                </>
              )}
              {selectedAsset.type === "POWER" && (
                <>
                  <div>Population Served: {selectedAsset.data.population_served.toLocaleString()}</div>
                  <div>Operational: {selectedAsset.data.is_operational ? "YES" : "DE-ENERGIZED"}</div>
                  <div>Flood Vulnerability: {selectedAsset.data.flood_risk}</div>
                </>
              )}
            </div>
          </div>
        )}

        {/* Map Legend (Bottom Right Overlay) */}
        <div className="absolute bottom-3 right-3 z-30 bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded px-2.5 py-1.5 flex items-center space-x-3 text-[10px] font-mono text-slate-300">
          <div className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded-full bg-red-600 inline-block" />
            <span>Impaired Hospital</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-600 inline-block" />
            <span>Active Hospital</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 bg-emerald-500 inline-block transform rotate-45" />
            <span>Shelter</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-3 h-0.5 bg-red-500 inline-block" />
            <span>Flooded Road</span>
          </div>
        </div>
      </div>
    </div>
  );
}
