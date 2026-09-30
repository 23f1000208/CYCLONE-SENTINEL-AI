from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from app.database.session import Base

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(50), primary_key=True, index=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=False)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    risk_score = Column(Float, nullable=False)          # 0.0 to 1.0
    risk_category = Column(String(30), nullable=False)   # LOW, MEDIUM, HIGH, EXTREME
    confidence_score = Column(Float, default=0.88)
    
    # Mathematical factor contributions (Zero-LLM explainability)
    hazard_score = Column(Float, nullable=False)
    exposure_score = Column(Float, nullable=False)
    vulnerability_score = Column(Float, nullable=False)
    
    contributing_factors = Column(JSON, nullable=False)  # Breakdown: surge, rain, elevation, roads, power
    formula_used = Column(String(200), default="Risk = Hazard * Exposure * Vulnerability")
    model_version = Column(String(50), default="Sentinel-Risk-v1.4")
    provenance_status = Column(String(30), default="MODELLED")
    
    assessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=False)
    
    # Scenario Controls
    wind_speed_kmh = Column(Float, nullable=False)
    rainfall_total_mm = Column(Float, nullable=False)
    storm_surge_m = Column(Float, nullable=False)
    landfall_lat = Column(Float, nullable=False)
    landfall_lon = Column(Float, nullable=False)
    
    is_baseline = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(String(50), primary_key=True, index=True)
    scenario_id = Column(String(50), ForeignKey("simulation_scenarios.id"), nullable=False)
    
    flooded_area_sqkm = Column(Float, nullable=False)
    flooded_area_increase_pct = Column(Float, default=0.0)
    
    exposed_population = Column(Integer, nullable=False)
    exposed_population_delta = Column(Integer, default=0)
    
    exposed_hospitals_count = Column(Integer, nullable=False)
    inaccessible_hospitals = Column(JSON, default=list)
    
    exposed_roads_count = Column(Integer, nullable=False)
    impassable_road_ids = Column(JSON, default=list)
    
    exposed_power_assets_count = Column(Integer, nullable=False)
    shelter_demand_total = Column(Integer, nullable=False)
    shelter_deficit = Column(Integer, default=0)
    
    inundation_geojson = Column(JSON, nullable=True)
    disclaimer = Column(String(200), default="MODELLED SCENARIO — NOT AN OFFICIAL FORECAST")
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
