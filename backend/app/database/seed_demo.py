import hashlib
import json
from datetime import datetime, timedelta, timezone
from app.database.session import engine, Base, SessionLocal
import app.models as models

def generate_checksum(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def seed_demo_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(models.CycloneEvent).filter_by(id="CYCLONE-DEMO-01").first()
        if existing:
            print("Demo data already seeded.")
            return

        now = datetime.now(timezone.utc)

        # 1. Geographic Region (Odisha Coast: Puri - Paradeep Corridor)
        region = models.GeographicRegion(
            id="REGION-ODISHA-COASTAL",
            name="Bay of Bengal Coastal Sector (Odisha Sector 4)",
            state="Odisha",
            country="India",
            boundary_geojson={
                "type": "Polygon",
                "coordinates": [[
                    [85.60, 19.65],
                    [86.85, 19.95],
                    [86.75, 20.45],
                    [85.85, 20.25],
                    [85.60, 19.65]
                ]]
            },
            center_lat=20.05,
            center_lon=86.25,
            total_area_sqkm=2450.0,
            average_elevation_m=4.2,
            coastline_length_km=94.5
        )
        db.add(region)

        # 2. Cyclone Event: CYCLONE DEMO-01
        cyclone = models.CycloneEvent(
            id="CYCLONE-DEMO-01",
            name="Cyclone DEMO-01",
            status="ACTIVE MONITORING",
            category="Very Severe Cyclonic Storm",
            basin="Bay of Bengal",
            current_lat=19.45,
            current_lon=86.80,
            current_wind_speed_kmh=140.0,
            current_pressure_hpa=968.0,
            movement_direction="Northwest",
            movement_speed_kmh=18.0,
            wind_radius_km=120.0,
            provenance_status="SYNTHETIC",
            provenance_source="Sentinel Disaster Simulation Engine (Bay of Bengal Model)",
            data_freshness="SIMULATED",
            last_updated=now,
            created_at=now - timedelta(hours=6)
        )
        db.add(cyclone)

        # 3. Forecast Observations (Trajectory & Forecast Cone)
        forecast_points = [
            (-12, 18.25, 87.60, 125.0, 978.0, 15.0),
            (-6, 18.85, 87.20, 135.0, 972.0, 20.0),
            (0, 19.45, 86.80, 140.0, 968.0, 25.0),    # Current
            (6, 20.05, 86.40, 145.0, 964.0, 35.0),    # Landfall Window
            (12, 20.55, 86.05, 130.0, 975.0, 50.0),
            (24, 21.30, 85.40, 85.0, 990.0, 75.0),
        ]
        for lead, lat, lon, wind, press, cone in forecast_points:
            db.add(models.ForecastObservation(
                cyclone_id="CYCLONE-DEMO-01",
                lead_time_hours=lead,
                valid_time=now + timedelta(hours=lead),
                lat=lat,
                lon=lon,
                wind_speed_kmh=wind,
                pressure_hpa=press,
                wind_radius_km=110.0 + (lead * 1.5 if lead > 0 else 0),
                cone_radius_km=cone,
                uncertainty_score=min(0.85, 0.10 + abs(lead) * 0.025),
                provenance_status="MODELLED"
            ))

        # 4. Population Zones
        zones_data = [
            ("ZONE-A", "Coastal Lowland Sector A (Puri Beachfront)", 68000, 850.0, 28.5, 19.80, 85.85, 3.2),
            ("ZONE-B", "Estuarine Delta Zone B (Astaranga - Konark)", 54000, 620.0, 31.0, 19.98, 86.15, 2.4),
            ("ZONE-C", "Port & Industrial Corridor C (Paradeep)", 82000, 1100.0, 19.5, 20.30, 86.60, 2.8),
            ("ZONE-D", "Inland Agricultural District D (Jagatsinghpur)", 115000, 780.0, 24.0, 20.25, 86.15, 6.8),
            ("ZONE-E", "North Estuary Basin E (Mahanadi Rivermouth)", 38000, 410.0, 34.0, 20.40, 86.70, 1.9),
        ]
        for zid, zname, pop, dens, vuln, lat, lon, elev in zones_data:
            db.add(models.PopulationZone(
                id=zid,
                region_id="REGION-ODISHA-COASTAL",
                zone_name=zname,
                total_population=pop,
                density_per_sqkm=dens,
                vulnerable_demographic_pct=vuln,
                boundary_geojson={
                    "type": "Polygon",
                    "coordinates": [[
                        [lon - 0.12, lat - 0.08],
                        [lon + 0.12, lat - 0.08],
                        [lon + 0.12, lat + 0.08],
                        [lon - 0.12, lat + 0.08],
                        [lon - 0.12, lat - 0.08]
                    ]]
                },
                exposed_population=int(pop * 0.72),
                high_risk_population=int(pop * 0.38),
                evacuation_zone_population=int(pop * 0.28),
                estimated_shelter_demand=int(pop * 0.22)
            ))

        # 5. Hospitals (12 facilities across coast & inland)
        hospitals_data = [
            ("H-101", "Paradeep Port Trust Hospital", 20.29, 86.62, 2.6, 220, 35, 72.0, True, 0.78),
            ("H-102", "Puri District Headquarters Hospital", 19.81, 85.83, 4.2, 350, 45, 60.0, True, 0.45),
            ("H-103", "Konark Sub-Divisional Hospital", 19.89, 86.12, 3.1, 110, 12, 48.0, False, 0.82), # Inaccessible
            ("H-104", "Jagatsinghpur Civil Hospital", 20.26, 86.17, 7.5, 280, 30, 96.0, True, 0.18),
            ("H-105", "Astaranga Community Health Center", 19.97, 86.27, 2.2, 60, 6, 24.0, False, 0.91), # Impaired
            ("H-106", "Kakatpur Rural Hospital", 20.02, 86.20, 4.8, 85, 8, 36.0, True, 0.35),
            ("H-107", "Ersama First Referral Unit", 20.18, 86.42, 2.5, 95, 10, 30.0, False, 0.85), # Inaccessible
            ("H-108", "Nimapada Sub-Divisional Hospital", 20.07, 85.98, 8.2, 140, 15, 72.0, True, 0.12),
            ("H-109", "Balikuda Community Hospital", 20.12, 86.32, 3.8, 70, 6, 36.0, True, 0.62),
            ("H-110", "Kujang Area Hospital", 20.31, 86.53, 3.5, 120, 14, 48.0, True, 0.58),
            ("H-111", "Brahmagiri Rural Health Center", 19.80, 85.65, 3.9, 50, 4, 24.0, True, 0.48),
            ("H-112", "Gop Model Hospital", 19.99, 86.02, 6.1, 80, 8, 48.0, True, 0.22),
        ]
        for hid, hname, lat, lon, elev, beds, icu, gen, access, inun in hospitals_data:
            db.add(models.Hospital(
                id=hid,
                name=hname,
                region_id="REGION-ODISHA-COASTAL",
                lat=lat,
                lon=lon,
                elevation_m=elev,
                bed_capacity=beds,
                icu_capacity=icu,
                emergency_generator_hours=gen,
                is_accessible=access,
                inundation_risk=inun,
                power_backup_functional=True
            ))
            # Also register in generic infrastructure_assets
            db.add(models.InfrastructureAsset(
                id=f"ASSET-{hid}",
                name=hname,
                asset_type="HOSPITAL",
                region_id="REGION-ODISHA-COASTAL",
                lat=lat,
                lon=lon,
                elevation_m=elev,
                criticality_score=0.95,
                flood_exposure_score=inun,
                status="OPERATIONAL" if access else "INACCESSIBLE"
            ))

        # 6. Cyclone Shelters (8 multipurpose multi-tier shelters)
        shelters_data = [
            ("S-201", "Puri Grand Road Multipurpose Cyclone Shelter", 19.82, 85.84, 9.5, 2500, True),
            ("S-202", "Astaranga Coastal High-Perch Shelter", 19.98, 86.26, 8.2, 1800, True),
            ("S-203", "Konark Marine Drive Refuge Hub", 19.90, 86.11, 7.8, 1400, True),
            ("S-204", "Paradeep Nehru Bangla Community Refuge", 20.30, 86.61, 8.9, 2200, True),
            ("S-205", "Ersama Resilient Block Shelter", 20.19, 86.41, 7.5, 1600, False),
            ("S-206", "Nuagarh Coastal Defense Center", 19.95, 86.22, 8.0, 1100, True),
            ("S-207", "Kujang Integrated Evacuation Complex", 20.32, 86.52, 9.1, 2000, True),
            ("S-208", "Gop Inland Central Refuge", 20.00, 86.01, 10.2, 1500, True),
        ]
        for sid, sname, lat, lon, elev, cap, med in shelters_data:
            db.add(models.Shelter(
                id=sid,
                name=sname,
                region_id="REGION-ODISHA-COASTAL",
                lat=lat,
                lon=lon,
                elevation_m=elev,
                total_capacity=cap,
                current_occupancy=int(cap * 0.15),
                expected_demand=int(cap * 0.85),
                medical_facility=med,
                drinking_water_days=7.0,
                is_safe=True,
                is_accessible=True
            ))

        # 7. Road Segments (45 interconnecting segments including NH-316, SH-13, Coastal Evacuation Corridors)
        # We generate structured segments with coordinates, elevations, and flood states
        for i in range(1, 46):
            base_lat = 19.70 + (i % 7) * 0.11
            base_lon = 85.75 + (i // 7) * 0.14
            elev = 1.8 + (i % 5) * 1.5
            coastal_dist = 1.2 + (i % 8) * 2.1
            is_corridor = (i % 3 == 0)
            is_flooded = (elev < 3.0 and coastal_dist < 4.0)

            db.add(models.RoadSegment(
                id=f"ROAD-{i:03d}",
                name=f"Corridor R-{i:02d} ({'National Highway' if i < 10 else 'Coastal Highway' if i < 25 else 'District Link'})",
                region_id="REGION-ODISHA-COASTAL",
                start_lat=round(base_lat, 4),
                start_lon=round(base_lon, 4),
                end_lat=round(base_lat + 0.05, 4),
                end_lon=round(base_lon + 0.06, 4),
                geometry_geojson={
                    "type": "LineString",
                    "coordinates": [
                        [round(base_lon, 4), round(base_lat, 4)],
                        [round(base_lon + 0.03, 4), round(base_lat + 0.02, 4)],
                        [round(base_lon + 0.06, 4), round(base_lat + 0.05, 4)]
                    ]
                },
                elevation_m=round(elev, 2),
                distance_to_coast_km=round(coastal_dist, 2),
                critical_evacuation_corridor=is_corridor,
                connects_to_hospital=(i % 4 == 0),
                passability_status="IMPASSABLE_FLOODED" if is_flooded else "PASSABLE",
                current_flood_depth_cm=48.0 if is_flooded else 0.0
            ))

        # 8. Power Infrastructure (15 substations and distribution nodes)
        power_assets = [
            ("PWR-01", "Paradeep Port 220kV Grid Substation", 20.30, 86.63, 2.5, 65000),
            ("PWR-02", "Puri Town 132kV Main Substation", 19.82, 85.82, 4.0, 95000),
            ("PWR-03", "Konark Coastal 33kV Distribution Substation", 19.89, 86.13, 2.8, 32000),
            ("PWR-04", "Astaranga Marine Substation", 19.98, 86.25, 2.1, 24000),
            ("PWR-05", "Jagatsinghpur Central 132kV Switching Station", 20.27, 86.16, 7.2, 110000),
            ("PWR-06", "Ersama Coastal Feeder", 20.19, 86.43, 2.4, 28000),
            ("PWR-07", "Kujang Industrial Substation", 20.32, 86.54, 3.4, 45000),
            ("PWR-08", "Nimapada Rural 33kV Grid", 20.08, 85.99, 7.9, 52000),
            ("PWR-09", "Balikuda 33kV Substation", 20.13, 86.33, 3.6, 29000),
            ("PWR-10", "Gop Switching Node", 20.01, 86.03, 5.8, 38000),
            ("PWR-11", "Chilika Coastal Feeder", 19.75, 85.60, 2.0, 18000),
            ("PWR-12", "Satyabadi Grid Node", 19.95, 85.80, 8.5, 42000),
            ("PWR-13", "Mahanadi Estuary Terminal", 20.38, 86.72, 1.9, 15000),
            ("PWR-14", "Brahmagiri Distribution Substation", 19.81, 85.66, 3.7, 34000),
            ("PWR-15", "Kakatpur Feeder Station", 20.03, 86.21, 4.5, 31000),
        ]
        for pid, pname, lat, lon, elev, pop in power_assets:
            db.add(models.PowerInfrastructure(
                id=pid,
                name=pname,
                facility_type="Substation",
                region_id="REGION-ODISHA-COASTAL",
                lat=lat,
                lon=lon,
                elevation_m=elev,
                population_served=pop,
                wind_threshold_kmh=130.0,
                surge_threshold_m=1.5,
                is_operational=(elev >= 2.5),
                flood_risk=round(max(0.1, 1.0 - (elev / 8.0)), 2)
            ))

        # 9. Baseline Risk Assessment
        risk_assessment = models.RiskAssessment(
            id="RISK-ASSESS-BASE-001",
            cyclone_id="CYCLONE-DEMO-01",
            region_id="REGION-ODISHA-COASTAL",
            risk_score=0.76,
            risk_category="HIGH",
            confidence_score=0.89,
            hazard_score=0.82,
            exposure_score=0.74,
            vulnerability_score=0.71,
            contributing_factors={
                "storm_surge_contribution": 0.28,
                "rainfall_contribution": 0.23,
                "low_elevation_contribution": 0.18,
                "road_inaccessibility_contribution": 0.16,
                "power_grid_exposure_contribution": 0.15
            },
            formula_used="Risk = 0.25*Cyclone + 0.20*Rain + 0.20*Surge + 0.15*Flood + 0.10*Infra + 0.10*Pop",
            model_version="Sentinel-Risk-Deterministic-v1.4",
            provenance_status="MODELLED"
        )
        db.add(risk_assessment)

        # 10. Baseline Alert (DRAFT - Requires Human Approval)
        alert = models.Alert(
            id="ALERT-DEMO-001",
            cyclone_id="CYCLONE-DEMO-01",
            region_id="REGION-ODISHA-COASTAL",
            risk_level="ORANGE",
            title="Anticipatory Action Advisory: High Coastal Surge and Inundation Threat",
            headline="Severe Cyclonic Storm DEMO-01 Tracking Towards Odisha Coast — Landfall Anticipated within 6-9 Hours",
            advisory_text=(
                "High modeled storm surge (2.5m) and extreme rainfall (180mm) pose severe inundation risks "
                "across coastal sectors Astaranga, Paradeep, and Ersama. Deterministic analysis identifies "
                "3 hospitals at elevated flood risk (H-103, H-105, H-107) and 14 inundated road segments. "
                "Disaster managers should review evacuation corridors towards inland high-perch shelters (S-201, S-208) "
                "and deploy secondary emergency generation to critical medical facilities."
            ),
            status="DRAFT",
            is_official_government_warning=False,
            disclaimer="MODELLED SCENARIO DECISION SUPPORT — NOT AN OFFICIAL GOVERNMENT WARNING"
        )
        db.add(alert)

        # 11. Initial Audit Log
        audit_payload = {
            "action": "SYSTEM_SEED_INITIALIZATION",
            "cyclone_id": "CYCLONE-DEMO-01",
            "region": "REGION-ODISHA-COASTAL",
            "wind_kmh": 140.0,
            "rainfall_mm": 180.0,
            "surge_m": 2.5
        }
        db.add(models.AuditLog(
            event_type="SEED_DATA",
            actor="SYSTEM_INIT",
            role="SYSTEM",
            action="INITIALIZE_CYCLONE_DEMO_01",
            target_entity="cyclone_events",
            target_id="CYCLONE-DEMO-01",
            details=audit_payload,
            checksum=generate_checksum(audit_payload)
        ))

        db.commit()
        print("Cyclone DEMO-01 synthetic dataset successfully seeded into database.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding demo data: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
