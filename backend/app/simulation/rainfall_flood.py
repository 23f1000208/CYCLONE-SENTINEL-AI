from typing import Dict, Any, List
import numpy as np

class RainfallFloodSimulationEngine:
    """
    Deterministic Rainfall Runoff & Surface Accumulation Engine.
    Executes hydrological runoff pipeline:
    Rainfall (mm) -> Surface Runoff Accumulation -> Low Elevation Flood Inundation -> 
    Road Inaccessibility -> Hospital Accessibility Impairment -> Emergency Response Impact.
    """
    DISCLAIMER = "MODELLED SCENARIO — NOT AN OFFICIAL FORECAST"

    @classmethod
    def run_rainfall_simulation(
        cls,
        rainfall_total_mm: float,
        soil_saturation_pct: float = 85.0, # Pre-storm antecedent moisture
        roads: List[Dict[str, Any]] = None,
        hospitals: List[Dict[str, Any]] = None,
        elevation_cutoff_m: float = 3.5
    ) -> Dict[str, Any]:
        roads = roads or []
        hospitals = hospitals or []

        # 1. Soil infiltration capacity vs Excess runoff
        # Curve Number runoff proxy (CN ~ 82 for coastal alluvium/clay)
        runoff_retention_s = 254.0 * (100.0 / 82.0 - 1.0) # ~ 55.7 mm
        initial_abstraction = 0.2 * runoff_retention_s     # ~ 11.1 mm
        
        if rainfall_total_mm > initial_abstraction:
            excess_runoff_mm = ((rainfall_total_mm - initial_abstraction) ** 2) / (
                rainfall_total_mm - initial_abstraction + runoff_retention_s
            )
        else:
            excess_runoff_mm = 0.0

        excess_runoff_mm = round(float(excess_runoff_mm), 1)

        # 2. Road Flooding Impact
        flooded_roads = []
        impassable_count = 0
        for r in roads:
            elev = r.get("elevation_m", 3.0)
            # Water accumulation inversely proportional to elevation
            water_depth_cm = max(0.0, round((excess_runoff_mm / 10.0) * (elevation_cutoff_m / max(0.5, elev)), 1))
            is_impassable = water_depth_cm > 30.0 # Standard vehicle passability threshold 30cm
            if is_impassable:
                impassable_count += 1
                flooded_roads.append({
                    "road_id": r["id"],
                    "name": r.get("name", r["id"]),
                    "water_depth_cm": water_depth_cm,
                    "elevation_m": elev
                })

        # 3. Hospital Accessibility Impact
        impacted_hospitals = []
        for h in hospitals:
            elev = h.get("elevation_m", 5.0)
            inundation_risk = round(min(1.0, (excess_runoff_mm / 220.0) * (elevation_cutoff_m / max(1.0, elev))), 2)
            is_accessible = (inundation_risk < 0.70)
            if not is_accessible:
                impacted_hospitals.append({
                    "hospital_id": h["id"],
                    "name": h["name"],
                    "inundation_risk": inundation_risk,
                    "elevation_m": elev,
                    "bed_capacity": h.get("bed_capacity", 100)
                })

        # 4. Total Flooded Area Estimate (sq km)
        flooded_area_sqkm = round(float(140.0 * (excess_runoff_mm / 100.0)), 1)

        return {
            "scenario_rainfall_mm": rainfall_total_mm,
            "excess_runoff_mm": excess_runoff_mm,
            "flooded_area_sqkm": flooded_area_sqkm,
            "total_roads_analyzed": len(roads),
            "impassable_roads_count": impassable_count,
            "flooded_roads": flooded_roads[:10], # Top 10 for structured summary
            "total_hospitals_analyzed": len(hospitals),
            "inaccessible_hospitals_count": len(impacted_hospitals),
            "inaccessible_hospitals": impacted_hospitals,
            "disclaimer": cls.DISCLAIMER,
            "provenance_status": "SIMULATED"
        }
