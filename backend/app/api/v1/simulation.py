from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database.session import get_db
from app.simulation.scenario_runner import ScenarioComparisonRunner

router = APIRouter(prefix="/simulation", tags=["What-If Scenario Simulation"])

class SimulationRequest(BaseModel):
    wind_speed_kmh: float = Field(default=160.0, ge=60.0, le=300.0)
    rainfall_total_mm: float = Field(default=234.0, ge=10.0, le=600.0)
    storm_surge_m: float = Field(default=3.2, ge=0.5, le=10.0)
    baseline_wind_speed_kmh: float = Field(default=140.0)
    baseline_rainfall_total_mm: float = Field(default=180.0)
    baseline_storm_surge_m: float = Field(default=2.5)

@router.post("")
def run_scenario_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    baseline_params = {
        "wind_speed_kmh": req.baseline_wind_speed_kmh,
        "rainfall_total_mm": req.baseline_rainfall_total_mm,
        "storm_surge_m": req.baseline_storm_surge_m
    }
    scenario_params = {
        "wind_speed_kmh": req.wind_speed_kmh,
        "rainfall_total_mm": req.rainfall_total_mm,
        "storm_surge_m": req.storm_surge_m
    }
    result = ScenarioComparisonRunner.compare_scenarios(db, baseline_params, scenario_params)
    return result
