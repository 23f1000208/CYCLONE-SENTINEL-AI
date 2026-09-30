import pytest
from app.database.session import SessionLocal
from app.simulation.storm_surge import StormSurgeSimulationEngine
from app.simulation.rainfall_flood import RainfallFloodSimulationEngine
from app.simulation.scenario_runner import ScenarioComparisonRunner

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_storm_surge_simulation():
    peak_surge = StormSurgeSimulationEngine.compute_peak_surge_height(140.0, 968.0)
    assert 2.0 <= peak_surge <= 4.0
    
    sim = StormSurgeSimulationEngine.run_surge_simulation(peak_surge, 20.0, 86.3)
    assert "inundation_area_sqkm" in sim
    assert sim["disclaimer"] == "MODELLED SCENARIO — NOT AN OFFICIAL FORECAST"

def test_rainfall_simulation_controls():
    # Test 50mm vs 200mm
    sim_50 = RainfallFloodSimulationEngine.run_rainfall_simulation(50.0)
    sim_200 = RainfallFloodSimulationEngine.run_rainfall_simulation(200.0)
    
    assert sim_200["excess_runoff_mm"] > sim_50["excess_runoff_mm"]
    assert sim_200["flooded_area_sqkm"] > sim_50["flooded_area_sqkm"]

def test_scenario_comparison_deltas(db_session):
    baseline = {"wind_speed_kmh": 140.0, "rainfall_total_mm": 180.0, "storm_surge_m": 2.5}
    scenario = {"wind_speed_kmh": 160.0, "rainfall_total_mm": 234.0, "storm_surge_m": 3.2}
    
    result = ScenarioComparisonRunner.compare_scenarios(db_session, baseline, scenario)
    deltas = result["deltas"]
    
    # Verify exact math
    expected_area_delta = round(result["scenario"]["flooded_area_sqkm"] - result["baseline"]["flooded_area_sqkm"], 1)
    assert deltas["flooded_area_delta_sqkm"] == expected_area_delta
    
    expected_pop_delta = result["scenario"]["exposed_population"] - result["baseline"]["exposed_population"]
    assert deltas["population_exposed_delta"] == expected_pop_delta
