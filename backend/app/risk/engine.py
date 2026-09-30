from datetime import datetime, timezone
from typing import Dict, Any, Tuple
import numpy as np
from app.risk.weights import RiskWeights, DEFAULT_RISK_WEIGHTS

class DeterministicRiskEngine:
    """
    Deterministic Scientific Risk Engine
    Follows strict Rule: ZERO-LLM ARITHMETIC.
    Calculates exact risk metrics, factor contributions, and confidence bounds.
    """
    MODEL_VERSION = "Sentinel-Risk-Deterministic-v1.4"
    FORMULA_BASE = "Risk = Hazard * Exposure * Vulnerability"
    FORMULA_WEIGHTED = (
        "Risk = w1*CycloneIntensity + w2*Rainfall + w3*StormSurge + "
        "w4*FloodRisk + w5*InfraVuln + w6*PopulationExposure"
    )

    @staticmethod
    def normalize_value(val: float, min_val: float, max_val: float) -> float:
        """Clamp and normalize value between 0.0 and 1.0"""
        if max_val <= min_val:
            return 0.0
        return float(np.clip((val - min_val) / (max_val - min_val), 0.0, 1.0))

    @classmethod
    def calculate_hazard_component(cls, wind_speed_kmh: float, rainfall_mm: float, storm_surge_m: float) -> Tuple[float, Dict[str, float]]:
        # Normalize: Wind (50-250 km/h), Rain (20-350 mm), Surge (0.5-6.0 m)
        norm_wind = cls.normalize_value(wind_speed_kmh, 50.0, 250.0)
        norm_rain = cls.normalize_value(rainfall_mm, 20.0, 350.0)
        norm_surge = cls.normalize_value(storm_surge_m, 0.5, 6.0)
        
        # Hazard is weighted average of dynamic physical perils
        hazard_score = float(0.40 * norm_wind + 0.35 * norm_rain + 0.25 * norm_surge)
        breakdown = {
            "norm_wind": round(norm_wind, 4),
            "norm_rain": round(norm_rain, 4),
            "norm_surge": round(norm_surge, 4),
            "hazard_score": round(hazard_score, 4)
        }
        return hazard_score, breakdown

    @classmethod
    def calculate_exposure_component(cls, exposed_pop_ratio: float, exposed_infra_ratio: float) -> float:
        score = 0.55 * float(np.clip(exposed_pop_ratio, 0.0, 1.0)) + 0.45 * float(np.clip(exposed_infra_ratio, 0.0, 1.0))
        return round(float(score), 4)

    @classmethod
    def calculate_vulnerability_component(
        cls,
        avg_elevation_m: float,
        road_inaccessible_ratio: float,
        vulnerable_pop_ratio: float
    ) -> float:
        # Inverted elevation: lower elevation = higher vulnerability (0m = 1.0, 15m = 0.0)
        elev_vuln = float(np.clip(1.0 - (avg_elevation_m / 15.0), 0.0, 1.0))
        vuln_score = (
            0.40 * elev_vuln
            + 0.35 * float(np.clip(road_inaccessible_ratio, 0.0, 1.0))
            + 0.25 * float(np.clip(vulnerable_pop_ratio, 0.0, 1.0))
        )
        return round(float(vuln_score), 4)

    @classmethod
    def assess_risk(
        cls,
        wind_speed_kmh: float,
        rainfall_mm: float,
        storm_surge_m: float,
        avg_elevation_m: float,
        exposed_pop_ratio: float,
        exposed_infra_ratio: float,
        road_inaccessible_ratio: float,
        vulnerable_pop_ratio: float,
        weights: RiskWeights = DEFAULT_RISK_WEIGHTS
    ) -> Dict[str, Any]:
        """
        Executes deterministic dual-model assessment:
        1. Core Multiplicative Model: Risk = Hazard * Exposure * Vulnerability
        2. Configurable Weighted Multi-Hazard Model
        """
        hazard_score, hazard_parts = cls.calculate_hazard_component(wind_speed_kmh, rainfall_mm, storm_surge_m)
        exposure_score = cls.calculate_exposure_component(exposed_pop_ratio, exposed_infra_ratio)
        vulnerability_score = cls.calculate_vulnerability_component(
            avg_elevation_m, road_inaccessible_ratio, vulnerable_pop_ratio
        )

        # Multiplicative baseline
        multiplicative_score = float(hazard_score * exposure_score * vulnerability_score)

        # Configurable Weighted Multi-Hazard formulation
        # w1*cyclone_intensity + w2*rainfall + w3*surge + w4*flood(elevation+rain) + w5*infra + w6*pop
        flood_risk_proxy = round(0.6 * hazard_parts["norm_rain"] + 0.4 * (1.0 - np.clip(avg_elevation_m / 15.0, 0, 1)), 4)
        
        weighted_score = (
            weights.cyclone_intensity * hazard_parts["norm_wind"]
            + weights.rainfall_risk * hazard_parts["norm_rain"]
            + weights.storm_surge_risk * hazard_parts["norm_surge"]
            + weights.flood_risk * flood_risk_proxy
            + weights.infrastructure_vulnerability * exposed_infra_ratio
            + weights.population_exposure * exposed_pop_ratio
        )
        final_risk = round(float(np.clip(weighted_score, 0.0, 1.0)), 4)

        # Determine category & color
        if final_risk < 0.25:
            category = "LOW"
            color_state = "GREEN"
            stage = "Active Monitoring"
        elif final_risk < 0.50:
            category = "MEDIUM"
            color_state = "YELLOW"
            stage = "Preparedness"
        elif final_risk < 0.75:
            category = "HIGH"
            color_state = "ORANGE"
            stage = "Enhanced Preparedness"
        else:
            category = "EXTREME"
            color_state = "RED"
            stage = "Emergency Preparedness"

        # Explicit contribution shares for zero-LLM explainability
        # Each factor's exact percentage contribution to the final risk score
        contributions = {
            "cyclone_wind": round(weights.cyclone_intensity * hazard_parts["norm_wind"], 4),
            "rainfall_inundation": round(weights.rainfall_risk * hazard_parts["norm_rain"], 4),
            "coastal_surge": round(weights.storm_surge_risk * hazard_parts["norm_surge"], 4),
            "flood_accumulation": round(weights.flood_risk * flood_risk_proxy, 4),
            "infrastructure_vulnerability": round(weights.infrastructure_vulnerability * exposed_infra_ratio, 4),
            "population_exposure": round(weights.population_exposure * exposed_pop_ratio, 4)
        }
        total_contrib = sum(contributions.values()) or 1.0
        contributions_pct = {
            k: round((v / total_contrib) * 100, 2) for k, v in contributions.items()
        }

        # Confidence estimation based on observation freshness and extremity
        confidence = round(float(np.clip(0.95 - (0.08 * hazard_score) + 0.05 * (1.0 - abs(0.5 - final_risk)), 0.65, 0.98)), 2)

        return {
            "risk_score": final_risk,
            "risk_category": category,
            "color_state": color_state,
            "operational_stage": stage,
            "confidence_score": confidence,
            "components": {
                "hazard_score": round(hazard_score, 4),
                "exposure_score": round(exposure_score, 4),
                "vulnerability_score": round(vulnerability_score, 4),
                "multiplicative_baseline": round(multiplicative_score, 4)
            },
            "contributing_factors": contributions,
            "contributions_percent": contributions_pct,
            "formula": cls.FORMULA_WEIGHTED,
            "model_version": cls.MODEL_VERSION,
            "provenance_status": "MODELLED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
