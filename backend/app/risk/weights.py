from pydantic import BaseModel, Field

class RiskWeights(BaseModel):
    cyclone_intensity: float = Field(default=0.25, ge=0.0, le=1.0)
    rainfall_risk: float = Field(default=0.20, ge=0.0, le=1.0)
    storm_surge_risk: float = Field(default=0.20, ge=0.0, le=1.0)
    flood_risk: float = Field(default=0.15, ge=0.0, le=1.0)
    infrastructure_vulnerability: float = Field(default=0.10, ge=0.0, le=1.0)
    population_exposure: float = Field(default=0.10, ge=0.0, le=1.0)

    def validate_sum(self) -> bool:
        total = (
            self.cyclone_intensity
            + self.rainfall_risk
            + self.storm_surge_risk
            + self.flood_risk
            + self.infrastructure_vulnerability
            + self.population_exposure
        )
        return abs(total - 1.0) < 1e-4

DEFAULT_RISK_WEIGHTS = RiskWeights()
