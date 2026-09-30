"use client";

import React, { useState, useEffect } from "react";
import KpiBar from "@/components/kpi/kpi-bar";
import CommandMap from "@/components/map/command-map";
import AiPanel from "@/components/ai/ai-panel";
import ScenarioSimulator from "@/components/simulation/scenario-simulator";
import HumanApprovalDrawer from "@/components/approval/human-approval-drawer";
import SitRepModal from "@/components/reports/sitrep-modal";

export default function CommandCenterPage() {
  const [cyclone, setCyclone] = useState<any>(null);
  const [hospitals, setHospitals] = useState<any[]>([]);
  const [shelters, setShelters] = useState<any[]>([]);
  const [roads, setRoads] = useState<any[]>([]);
  const [power, setPower] = useState<any[]>([]);
  const [advisories, setAdvisories] = useState<any[]>([]);
  const [risk, setRisk] = useState<any>(null);

  const [isApprovalOpen, setIsApprovalOpen] = useState(false);
  const [isSitRepOpen, setIsSitRepOpen] = useState(false);
  const [selectedAdvisory, setSelectedAdvisory] = useState<any>(null);

  const fetchData = async () => {
    try {
      const [cRes, hRes, sRes, rRes, pRes, aRes, rkRes] = await Promise.all([
        fetch("/api/v1/cyclones/CYCLONE-DEMO-01"),
        fetch("/api/v1/infrastructure/hospitals"),
        fetch("/api/v1/infrastructure/shelters"),
        fetch("/api/v1/infrastructure/roads"),
        fetch("/api/v1/infrastructure/power"),
        fetch("/api/v1/advisories"),
        fetch("/api/v1/risk"),
      ]);

      if (cRes.ok) setCyclone(await cRes.json());
      if (hRes.ok) setHospitals(await hRes.json());
      if (sRes.ok) setShelters(await sRes.json());
      if (rRes.ok) setRoads(await rRes.json());
      if (pRes.ok) setPower(await pRes.json());
      if (aRes.ok) {
        const advs = await aRes.json();
        setAdvisories(advs);
        if (advs.length > 0) setSelectedAdvisory(advs[0]);
      }
      if (rkRes.ok) setRisk(await rkRes.json());
    } catch (e) {
      console.warn("Using offline fallback data for command center rendering", e);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const kpiData = {
    windSpeedKmh: cyclone?.current_wind_speed_kmh || 140,
    pressureHpa: cyclone?.current_pressure_hpa || 968,
    rainfallMm: 180,
    stormSurgeM: 2.5,
    exposedPopulation: 248000,
    exposedInfraCount: 18,
    atRiskHospitals: 3,
    riskCategory: risk?.risk_category || "HIGH",
  };

  return (
    <div className="flex-1 flex flex-col space-y-4 p-4 lg:p-6 bg-[#080d16]">
      {/* 1. TOP KPIS BAR */}
      <KpiBar data={kpiData} />

      {/* 2. MAIN MAP & AI SUPERVISOR GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Geospatial Map Canvas (7 cols) */}
        <div className="lg:col-span-7 flex flex-col">
          <CommandMap
            cycloneData={cyclone}
            hospitals={hospitals}
            shelters={shelters}
            roads={roads}
            power={power}
            surgeData={null}
          />
        </div>

        {/* Explainable AI Supervisor Panel (5 cols) */}
        <div className="lg:col-span-5 h-[540px]">
          <AiPanel
            riskData={risk}
            onAdvisoryReview={() => setIsApprovalOpen(true)}
            onGenerateReport={() => setIsSitRepOpen(true)}
          />
        </div>
      </div>

      {/* 3. WHAT-IF SCENARIO SIMULATOR (Bottom) */}
      <ScenarioSimulator />

      {/* 4. MODALS & DRAWERS */}
      <HumanApprovalDrawer
        isOpen={isApprovalOpen}
        onClose={() => setIsApprovalOpen(false)}
        advisory={selectedAdvisory}
        onActionComplete={fetchData}
      />

      <SitRepModal
        isOpen={isSitRepOpen}
        onClose={() => setIsSitRepOpen(false)}
        cyclone={cyclone}
        risk={risk}
      />
    </div>
  );
}
