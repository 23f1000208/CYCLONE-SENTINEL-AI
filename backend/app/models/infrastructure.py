from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from app.database.session import Base

class InfrastructureAsset(Base):
    __tablename__ = "infrastructure_assets"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    asset_type = Column(String(50), nullable=False)  # HOSPITAL, SHELTER, ROAD, POWER, BRIDGE
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    elevation_m = Column(Float, default=3.2)
    distance_to_coast_km = Column(Float, default=4.5)
    criticality_score = Column(Float, default=0.8)  # 0 to 1
    
    # Current vulnerability assessment state
    flood_exposure_score = Column(Float, default=0.0)
    wind_exposure_score = Column(Float, default=0.0)
    surge_exposure_score = Column(Float, default=0.0)
    overall_vulnerability_score = Column(Float, default=0.0)
    status = Column(String(50), default="OPERATIONAL")  # OPERATIONAL, IMPAIRED, INACCESSIBLE, CRITICAL

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    elevation_m = Column(Float, default=5.0)
    
    bed_capacity = Column(Integer, default=150)
    icu_capacity = Column(Integer, default=20)
    emergency_generator_hours = Column(Float, default=48.0)
    access_road_id = Column(String(50), nullable=True)
    alternate_hospital_id = Column(String(50), nullable=True)
    
    is_accessible = Column(Boolean, default=True)
    inundation_risk = Column(Float, default=0.2)
    power_backup_functional = Column(Boolean, default=True)

class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    elevation_m = Column(Float, default=8.5)
    
    total_capacity = Column(Integer, default=1200)
    current_occupancy = Column(Integer, default=0)
    expected_demand = Column(Integer, default=0)
    medical_facility = Column(Boolean, default=True)
    drinking_water_days = Column(Float, default=5.0)
    
    is_safe = Column(Boolean, default=True)
    is_accessible = Column(Boolean, default=True)

class RoadSegment(Base):
    __tablename__ = "road_segments"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lon = Column(Float, nullable=False)
    geometry_geojson = Column(JSON, nullable=False)  # LineString GeoJSON
    
    elevation_m = Column(Float, default=2.5)
    distance_to_coast_km = Column(Float, default=1.8)
    critical_evacuation_corridor = Column(Boolean, default=False)
    connects_to_hospital = Column(Boolean, default=False)
    
    passability_status = Column(String(30), default="PASSABLE")  # PASSABLE, RESTRICTED, IMPASSABLE_FLOODED
    current_flood_depth_cm = Column(Float, default=0.0)

class PowerInfrastructure(Base):
    __tablename__ = "power_infrastructure"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    facility_type = Column(String(50), default="Substation")  # Substation, Transmission Line, Generator
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    elevation_m = Column(Float, default=3.0)
    population_served = Column(Integer, default=45000)
    
    wind_threshold_kmh = Column(Float, default=130.0)
    surge_threshold_m = Column(Float, default=1.5)
    is_operational = Column(Boolean, default=True)
    flood_risk = Column(Float, default=0.25)
