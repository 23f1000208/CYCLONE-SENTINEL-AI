from typing import Dict, Any, List
from sqlalchemy.orm import Session
import app.models as models
from app.simulation.storm_surge import StormSurgeSimulationEngine
from app.simulation.rainfall_flood import RainfallFloodSimulationEngine

class ScenarioComparisonRunner:
    """
    Deterministic What-If Scenario Comparator.
    Evaluates:
    BASELINE vs SCENARIO
    and computes exact numerical deltas for zero-LLM arithmetic compliance.
    """
    DISCLAIMER = "MODELLED SCENARIO — NOT AN OFFICIAL FORECAST"

    @classmethod
    def compare_scenarios(
        cls,
        db: Session,
        baseline_params: Dict[str, float],
        scenario_params: Dict[str, float]
    ) -> Dict[str, Any]:
        # Query infrastructure from DB
        hospitals = db.query(models.Hospital).all()
        roads = db.query(models.RoadSegment).all()
        shelters = db.query(models.Shelter).all()
        power = db.query(models.PowerInfrastructure).all()
        zones = db.query(models.PopulationZone).all()

        h_dicts = [{"id": h.id, "name": h.name, "elevation_m": h.elevation_m, "bed_capacity": h.bed_capacity} for h in hospitals]
        r_dicts = [{"id": r.id, "name": r.name, "elevation_m": r.elevation_m} for r in roads]

        # 1. Run Baseline
        base_wind = baseline_params.get("wind_speed_kmh", 140.0)
        base_rain = baseline_params.get("rainfall_total_mm", 180.0)
        base_surge = baseline_params.get("storm_surge_m", 2.5)

        base_surge_sim = StormSurgeSimulationEngine.run_surge_simulation(base_surge, 20.0, 86.3)
        base_rain_sim = RainfallFloodSimulationEngine.run_rainfall_simulation(base_rain, roads=r_dicts, hospitals=h_dicts)

        total_pop = sum(z.total_population for z in zones) or 357000
        base_exposed_pop = int(total_pop * min(0.95, 0.40 + 0.0015 * base_rain + 0.05 * base_surge))
        base_shelter_demand = int(base_exposed_pop * 0.28)
        base_power_exposed = sum(1 for p in power if p.elevation_m < (base_surge + 1.2))

        base_flooded_area = base_surge_sim["inundation_area_sqkm"] + base_rain_sim["flooded_area_sqkm"]

        # 2. Run Scenario
        scen_wind = scenario_params.get("wind_speed_kmh", 160.0)
        scen_rain = scenario_params.get("rainfall_total_mm", 234.0)
        scen_surge = scenario_params.get("storm_surge_m", 3.2)

        scen_surge_sim = StormSurgeSimulationEngine.run_surge_simulation(scen_surge, 20.0, 86.3)
        scen_rain_sim = RainfallFloodSimulationEngine.run_rainfall_simulation(scen_rain, roads=r_dicts, hospitals=h_dicts)

        scen_exposed_pop = int(total_pop * min(0.98, 0.40 + 0.0015 * scen_rain + 0.05 * scen_surge))
        scen_shelter_demand = int(scen_exposed_pop * 0.32)
        scen_power_exposed = sum(1 for p in power if p.elevation_m < (scen_surge + 1.2))

        scen_flooded_area = scen_surge_sim["inundation_area_sqkm"] + scen_rain_sim["flooded_area_sqkm"]

        # 3. Deterministic Delta Calculations (Zero-LLM Arithmetic)
        flooded_area_delta = round(scen_flooded_area - base_flooded_area, 1)
        flooded_area_pct = round(((scen_flooded_area - base_flooded_area) / max(1.0, base_flooded_area)) * 100, 2)

        pop_delta = scen_exposed_pop - base_exposed_pop
        pop_pct = round((pop_delta / max(1.0, base_exposed_pop)) * 100, 2)

        roads_delta = scen_rain_sim["impassable_roads_count"] - base_rain_sim["impassable_roads_count"]
        hospitals_delta = scen_rain_sim["inaccessible_hospitals_count"] - base_rain_sim["inaccessible_hospitals_count"]
        power_delta = scen_power_exposed - base_power_exposed
        shelter_demand_delta = scen_shelter_demand - base_shelter_demand

        return {
            "baseline": {
                "wind_speed_kmh": base_wind,
                "rainfall_mm": base_rain,
                "storm_surge_m": base_surge,
                "flooded_area_sqkm": base_flooded_area,
                "exposed_population": base_exposed_pop,
                "impassable_roads": base_rain_sim["impassable_roads_count"],
                "inaccessible_hospitals": base_rain_sim["inaccessible_hospitals_count"],
                "exposed_power_assets": base_power_exposed,
                "shelter_demand": base_shelter_demand
            },
            "scenario": {
                "wind_speed_kmh": scen_wind,
                "rainfall_mm": scen_rain,
                "storm_surge_m": scen_surge,
                "flooded_area_sqkm": scen_flooded_area,
                "exposed_population": scen_exposed_pop,
                "impassable_roads": scen_rain_sim["impassable_roads_count"],
                "inaccessible_hospitals": scen_rain_sim["inaccessible_hospitals_count"],
                "exposed_power_assets": scen_power_exposed,
                "shelter_demand": scen_shelter_demand
            },
            "deltas": {
                "flooded_area_delta_sqkm": flooded_area_delta,
                "flooded_area_change_pct": flooded_area_pct,
                "population_exposed_delta": pop_delta,
                "population_exposed_change_pct": pop_pct,
                "additional_roads_flooded": roads_delta,
                "additional_hospitals_inaccessible": hospitals_delta,
                "additional_power_assets_exposed": power_delta,
                "additional_shelter_demand": shelter_demand_delta
            },
            "disclaimer": cls.DISCLAIMER,
            "provenance_status": "SIMULATED"
        }
