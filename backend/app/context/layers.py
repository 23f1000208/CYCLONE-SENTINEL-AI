from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SystemContext(BaseModel):
    agent_role: str = "Disaster Intelligence Supervisor Agent"
    boundaries: str = "Zero-LLM arithmetic strictly enforced. Operational actions require authorized human approval."
    authorized_permissions: List[str] = ["ANALYZE", "SIMULATE", "COMPARE", "RECOMMEND", "DRAFT_ADVISORY"]
    prohibited_actions: List[str] = [
        "ISSUE_OFFICIAL_EVACUATION_ORDERS",
        "DISPATCH_EMERGENCY_TEAMS",
        "SHUT_DOWN_GRID",
        "INVENT_NUMBERS_OR_ASSET_IDS"
    ]

class EventContext(BaseModel):
    event_id: str
    event_name: str
    status: str
    category: str
    basin: str
    current_lat: float
    current_lon: float
    wind_speed_kmh: float
    pressure_hpa: float
    movement: str
    data_freshness: str
    provenance_status: str

class SpatialContext(BaseModel):
    region_id: str
    bounding_box: Dict[str, float]
    nearby_hospitals: List[Dict[str, Any]]
    nearby_shelters: List[Dict[str, Any]]
    critical_roads: List[Dict[str, Any]]
    power_nodes: List[Dict[str, Any]]

class AnalyticalContext(BaseModel):
    risk_score: float
    risk_category: str
    color_state: str
    confidence_score: float
    contributing_factors: Dict[str, float]
    contributions_percent: Dict[str, float]
    storm_surge_m: float
    rainfall_mm: float
    flooded_area_sqkm: float
    exposed_population: int
    impassable_roads_count: int
    inaccessible_hospitals_count: int

class TemporalContext(BaseModel):
    current_timestamp: str
    lead_time_hours: int
    risk_trend: str
    risk_change_percent: Optional[float] = None
    provenance_chain: List[str] = []

class StructuredContextEnvelope(BaseModel):
    """
    Standardized 5-Layer Context Envelope delivered to Agent & Gemini.
    Guarantees strict context engineering, spatial bounds, and provenance tracking.
    """
    system: SystemContext = Field(default_factory=SystemContext)
    event: EventContext
    spatial: SpatialContext
    analytical: AnalyticalContext
    temporal: TemporalContext
    compression_ratio: float = 0.85
    provenance_disclaimer: str = "MODELLED CONTEXT — PROVENANCE GROUNDED"
