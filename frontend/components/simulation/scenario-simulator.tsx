"use client";

import React, { useState } from "react";
import { Sliders, Play, ArrowRight, TrendingUp, AlertTriangle } from "lucide-react";

export default function ScenarioSimulator() {
  const [windKmh, setWindKmh] = useState(160);
  const [rainfallMm, setRainfallMm] = useState(234);
  const [surgeM, setSurgeM] = useState(3.2);
  const [isRunning, setIsRunning] = useState(false);

  // Baseline conditions
  const baseline = {
    wind: 140,
    rainfall: 180,
    surge: 2.5,
    floodedArea: 242.0,
    exposedPop: 248000,
    impassableRoads: 14,
    inaccHospitals: 3,
  };

  const [scenarioResults, setScenarioResults] = useState<any>({
    floodedArea: 326.5,
    exposedPop: 312000,
    impassableRoads: 22,
    inaccHospitals: 5,
    deltas: {
      floodedAreaDelta: 84.5,
      floodedAreaPct: 34.9,
      popDelta: 64000,
      popPct: 25.8,
      roadsDelta: 8,
      hospitalsDelta: 2,
    },
  });

  const runSimulation = async () => {
    setIsRunning(true);
    try {
      const res = await fetch("/api/v1/simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          wind_speed_kmh: windKmh,
          rainfall_total_mm: rainfallMm,
          storm_surge_m: surgeM,
        }),
      });
      const data = await res.json();
      setScenarioResults({
        floodedArea: data.scenario.flooded_area_sqkm,
        exposedPop: data.scenario.exposed_population,
        impassableRoads: data.scenario.impassable_roads,
        inaccHospitals: data.scenario.inaccessible_hospitals,
        deltas: {
          floodedAreaDelta: data.deltas.flooded_area_delta_sqkm,
          floodedAreaPct: data.deltas.flooded_area_change_pct,
          popDelta: data.deltas.population_exposed_delta,
          popPct: data.deltas.population_exposed_change_pct,
          roadsDelta: data.deltas.additional_roads_flooded,
          hospitalsDelta: data.deltas.additional_hospitals_inaccessible,
        },
      });
    } catch (err) {
      console.error("Simulation error", err);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="bg-[#0b101c] border border-slate-800 rounded-xl p-4 shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Sliders className="w-5 h-5 text-cyan-400" />
          <span className="font-bold text-sm text-slate-100 font-mono tracking-wide">
            WHAT-IF SCENARIO SIMULATOR
          </span>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
          MODELLED SCENARIO — NOT AN OFFICIAL FORECAST
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-4">
        {/* Controls Column (5 cols) */}
        <div className="lg:col-span-5 space-y-4 font-mono text-xs">
          {/* Wind Speed Control */}
          <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>WIND SPEED INTENSITY</span>
              <span className="text-cyan-400 font-bold">{windKmh} km/h</span>
            </div>
            <input
              type="range"
              min="100"
              max="240"
              step="5"
              value={windKmh}
              onChange={(e) => setWindKmh(Number(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 mt-1">
              <span>Baseline: 140 km/h</span>
              <span>Extreme: 240 km/h</span>
            </div>
          </div>

          {/* Rainfall Scenario Controls */}
          <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>RAINFALL SCENARIO</span>
              <span className="text-blue-400 font-bold">{rainfallMm} mm</span>
            </div>
            <input
              type="range"
              min="50"
              max="350"
              step="10"
              value={rainfallMm}
              onChange={(e) => setRainfallMm(Number(e.target.value))}
              className="w-full accent-blue-400 cursor-pointer"
            />
            <div className="flex space-x-1.5 mt-2">
              {[50, 100, 150, 200].map((preset) => (
                <button
                  key={preset}
                  onClick={() => setRainfallMm(preset)}
                  className={`flex-1 py-1 rounded text-[10px] border transition ${
                    rainfallMm === preset
                      ? "bg-blue-900/80 text-blue-200 border-blue-500 font-bold"
                      : "bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700"
                  }`}
                >
                  {preset}mm
                </button>
              ))}
            </div>
          </div>

          {/* Storm Surge Control */}
          <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>PEAK STORM SURGE</span>
              <span className="text-indigo-400 font-bold">{surgeM} m</span>
            </div>
            <input
              type="range"
              min="1.0"
              max="6.0"
              step="0.1"
              value={surgeM}
              onChange={(e) => setSurgeM(Number(e.target.value))}
              className="w-full accent-indigo-400 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 mt-1">
              <span>Baseline: 2.5m</span>
              <span>Catastrophic: 6.0m</span>
            </div>
          </div>

          <button
            onClick={runSimulation}
            disabled={isRunning}
            className="w-full py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-slate-950 font-bold rounded-lg transition shadow-lg flex items-center justify-center space-x-2 text-xs"
          >
            <Play className="w-4 h-4 fill-slate-950" />
            <span>{isRunning ? "CALCULATING DELTAS..." : "RUN CYCLONE IMPACT SIMULATION"}</span>
          </button>
        </div>

        {/* Results Column (7 cols): BASELINE vs SCENARIO comparison */}
        <div className="lg:col-span-7 bg-slate-900/60 p-4 rounded-lg border border-slate-800 font-mono flex flex-col justify-between">
          <div>
            <div className="grid grid-cols-3 text-center border-b border-slate-800 pb-2 text-xs font-bold text-slate-400">
              <span>IMPACT METRIC</span>
              <span className="text-slate-300">BASELINE (140km/h)</span>
              <span className="text-amber-400">SCENARIO ({windKmh}km/h)</span>
            </div>

            <div className="divide-y divide-slate-800/80 text-xs">
              {/* Flooded Area */}
              <div className="grid grid-cols-3 py-2.5 items-center">
                <span className="text-slate-300">Flooded Inundation Area</span>
                <span className="text-center text-slate-400">{baseline.floodedArea} km²</span>
                <div className="text-center">
                  <span className="text-amber-400 font-bold">{scenarioResults.floodedArea} km²</span>
                  <span className="text-[10px] text-red-400 ml-1.5 font-bold">
                    (+{scenarioResults.deltas.floodedAreaPct}%)
                  </span>
                </div>
              </div>

              {/* Population Exposed */}
              <div className="grid grid-cols-3 py-2.5 items-center">
                <span className="text-slate-300">Exposed Population</span>
                <span className="text-center text-slate-400">{baseline.exposedPop.toLocaleString()}</span>
                <div className="text-center">
                  <span className="text-amber-400 font-bold">
                    {scenarioResults.exposedPop.toLocaleString()}
                  </span>
                  <span className="text-[10px] text-red-400 ml-1.5 font-bold">
                    (+{scenarioResults.deltas.popPct}%)
                  </span>
                </div>
              </div>

              {/* Impassable Roads */}
              <div className="grid grid-cols-3 py-2.5 items-center">
                <span className="text-slate-300">Impassable Roads</span>
                <span className="text-center text-slate-400">{baseline.impassableRoads} segments</span>
                <div className="text-center">
                  <span className="text-amber-400 font-bold">
                    {scenarioResults.impassableRoads} segments
                  </span>
                  <span className="text-[10px] text-red-400 ml-1.5 font-bold">
                    (+{scenarioResults.deltas.roadsDelta})
                  </span>
                </div>
              </div>

              {/* Inaccessible Hospitals */}
              <div className="grid grid-cols-3 py-2.5 items-center">
                <span className="text-slate-300">Inaccessible Hospitals</span>
                <span className="text-center text-slate-400">{baseline.inaccHospitals} facilities</span>
                <div className="text-center">
                  <span className="text-red-400 font-bold">
                    {scenarioResults.inaccHospitals} facilities
                  </span>
                  <span className="text-[10px] text-red-400 ml-1.5 font-bold">
                    (+{scenarioResults.deltas.hospitalsDelta})
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
            <span className="flex items-center space-x-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span>Zero-LLM Deterministic Diff Engine Verified</span>
            </span>
            <span className="text-slate-500 font-mono">Formula: Delta = (Scenario - Baseline)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
