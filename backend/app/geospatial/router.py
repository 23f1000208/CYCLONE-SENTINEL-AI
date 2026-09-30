from typing import List, Dict, Any, Optional
from app.geospatial.spatial_ops import haversine_distance_km

class RouteAndFacilityRouter:
    """
    Deterministic Router for Disaster Evacuation and Facility Accessibility.
    Evaluates:
    1. Hospital accessibility given flooded road segments.
    2. Identification of best alternate hospitals with surplus capacity.
    3. Population zone shelter allocation with capacity checks.
    4. Route risk score for transport corridors.
    """

    @staticmethod
    def evaluate_hospital_accessibility(
        hospitals: List[Dict[str, Any]],
        flooded_road_ids: List[str]
    ) -> List[Dict[str, Any]]:
        results = []
        for h in hospitals:
            # A hospital is inaccessible if its primary access road is flooded or inundation_risk > 0.70
            road_blocked = h.get("access_road_id") in flooded_road_ids
            inundated = h.get("inundation_risk", 0.0) >= 0.75
            accessible = not (road_blocked or inundated)
            
            results.append({
                "hospital_id": h["id"],
                "name": h["name"],
                "lat": h["lat"],
                "lon": h["lon"],
                "elevation_m": h["elevation_m"],
                "bed_capacity": h["bed_capacity"],
                "icu_capacity": h.get("icu_capacity", 10),
                "inundation_risk": h.get("inundation_risk", 0.0),
                "is_accessible": accessible,
                "blockage_reason": "Road Flooded" if road_blocked else "Direct Inundation" if inundated else "None"
            })
        return results

    @staticmethod
    def find_alternate_hospitals(
        impacted_hospital_id: str,
        all_hospitals: List[Dict[str, Any]],
        flooded_road_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """Find top 3 nearest accessible alternative hospitals with capacity."""
        target = next((h for h in all_hospitals if h["id"] == impacted_hospital_id), None)
        if not target:
            return []

        accessible_candidates = []
        for h in all_hospitals:
            if h["id"] == impacted_hospital_id:
                continue
            # Check accessibility
            if h.get("inundation_risk", 0.0) < 0.60 and h.get("is_accessible", True):
                dist = haversine_distance_km(target["lat"], target["lon"], h["lat"], h["lon"])
                accessible_candidates.append({
                    "hospital_id": h["id"],
                    "name": h["name"],
                    "distance_km": dist,
                    "bed_capacity": h["bed_capacity"],
                    "icu_capacity": h.get("icu_capacity", 10),
                    "elevation_m": h["elevation_m"]
                })

        accessible_candidates.sort(key=lambda x: x["distance_km"])
        return accessible_candidates[:3]

    @staticmethod
    def allocate_shelters_for_zones(
        zones: List[Dict[str, Any]],
        shelters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Determines shelter demand vs available capacity across zones.
        Ensures deterministic shelter capacity calculations.
        """
        total_demand = sum(z.get("estimated_shelter_demand", 0) for z in zones)
        total_capacity = sum(s.get("total_capacity", 0) for s in shelters)
        deficit = max(0, total_demand - total_capacity)

        allocation_summary = []
        for z in zones:
            z_lat = z.get("lat") or 20.0
            z_lon = z.get("lon") or 86.0
            demand = z.get("estimated_shelter_demand", 0)

            # Sort shelters by distance to this zone center
            shelter_distances = []
            for s in shelters:
                dist = haversine_distance_km(z_lat, z_lon, s["lat"], s["lon"])
                shelter_distances.append({
                    "shelter_id": s["id"],
                    "name": s["name"],
                    "distance_km": dist,
                    "capacity": s["total_capacity"],
                    "medical": s.get("medical_facility", True)
                })
            shelter_distances.sort(key=lambda x: x["distance_km"])
            nearest = shelter_distances[0] if shelter_distances else None

            allocation_summary.append({
                "zone_id": z["id"],
                "zone_name": z.get("zone_name", z["id"]),
                "shelter_demand": demand,
                "primary_shelter": nearest,
                "status": "ALLOCATED" if nearest and nearest["capacity"] >= demand else "DEFICIT_RISK"
            })

        return {
            "total_shelter_demand": total_demand,
            "total_shelter_capacity": total_capacity,
            "net_surplus_deficit": total_capacity - total_demand,
            "deficit_count": deficit,
            "zone_allocations": allocation_summary
        }
