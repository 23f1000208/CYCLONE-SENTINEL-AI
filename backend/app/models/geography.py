from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from app.database.session import Base

class GeographicRegion(Base):
    __tablename__ = "geographic_regions"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state = Column(String(50), default="Odisha")
    country = Column(String(50), default="India")
    
    boundary_geojson = Column(JSON, nullable=False)  # GeoJSON Polygon / MultiPolygon
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    total_area_sqkm = Column(Float, default=150.0)
    average_elevation_m = Column(Float, default=4.5)
    coastline_length_km = Column(Float, default=28.0)

class PopulationZone(Base):
    __tablename__ = "population_zones"

    id = Column(String(50), primary_key=True, index=True)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    zone_name = Column(String(100), nullable=False)
    
    total_population = Column(Integer, nullable=False)
    density_per_sqkm = Column(Float, nullable=False)
    vulnerable_demographic_pct = Column(Float, default=24.5)  # Elderly, children, mobility-impaired
    boundary_geojson = Column(JSON, nullable=False)
    
    # Calculated / Dynamic exposure fields
    exposed_population = Column(Integer, default=0)
    high_risk_population = Column(Integer, default=0)
    evacuation_zone_population = Column(Integer, default=0)
    estimated_shelter_demand = Column(Integer, default=0)

class HazardZone(Base):
    __tablename__ = "hazard_zones"

    id = Column(String(50), primary_key=True, index=True)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    hazard_type = Column(String(50), nullable=False)  # STORM_SURGE, FLASH_FLOOD, WIND_SWATH
    severity_level = Column(String(20), default="HIGH")  # LOW, MEDIUM, HIGH, EXTREME
    
    return_period_years = Column(Integer, default=25)
    inundation_depth_m = Column(Float, default=1.8)
    geometry_geojson = Column(JSON, nullable=False)
