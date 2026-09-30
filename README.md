# CYCLONE SENTINEL AI
> **Track 5 — Cyclone Impact & Infrastructure Vulnerability Forecaster**  
> *"Predict the Impact. Protect the Infrastructure. Act Before Landfall."*

[![Backend Tests](https://img.shields.io/badge/Backend%20Tests-29%2F29%20Passed-emerald.svg)](#testing)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js%2014-cyan.svg)](#frontend)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](#backend)
[![Zero-LLM Arithmetic](https://img.shields.io/badge/Arithmetic-Deterministic%20Verified-purple.svg)](#architectural-philosophy)

---

## 1. Executive Summary & Problem Statement

Extreme weather events across the Bay of Bengal and coastal APAC require rapid anticipatory action. Historically, disaster response has suffered from being reactive: post-landfall recovery rather than proactive pre-landfall intervention.

**CYCLONE SENTINEL AI** is a production-grade decision-support platform designed to shift disaster management from:
$$\text{POST-LANDFALL RECOVERY} \longrightarrow \text{PRE-LANDFALL PREDICTIVE RISK} \longrightarrow \text{INFRASTRUCTURE VULNERABILITY} \longrightarrow \text{SCENARIO SIMULATION} \longrightarrow \text{HUMAN-APPROVED ADVISORIES}$$

---

## 2. Architectural Philosophy: Zero-LLM Arithmetic

A core principle of Cyclone Sentinel AI is that **LLMs must NEVER calculate or invent numbers**. 

```
[SATELLITE & SENSOR FEEDS] (GEE / GPM IMERG / Radar / GIS)
               │
               ▼
[DETERMINISTIC ENGINES] (NumPy / Shapely / GeoPandas / SciPy)
 ├── Risk Engine: Risk = Hazard × Exposure × Vulnerability
 ├── Hydrodynamic Storm Surge Model (SLOSH Parametric)
 ├── Hydrologic Runoff Accumulation Model
 └── Facility Accessibility & Routing Engine
               │
               ▼
[CONTEXT ENGINEERING LAYER] (5 Layers: Spatial/Temporal bounds, provenance tracking)
               │
               ▼
[GOOGLE ADK SUPERVISOR AGENT] (Bounded Tool Loop: Max 5 Iterations, 17 Typed Tools)
               │
               ▼
[GEMINI MULTIMODAL REASONING] (Qualitative interpretation & contextual explanation)
               │
               ▼
[OUTPUT & CAUSALITY VALIDATION] (Strict numeric verification & asset claim checking)
               │
               ▼
[HUMAN-IN-THE-LOOP APPROVAL] (Disaster Manager: APPROVE / MODIFY / REJECT)
               │
               ▼
[TAMPER-EVIDENT AUDIT TRAIL] (SHA-256 Chained Hash Log)
```

---

## 3. Technology Stack

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons, Recharts, Interactive WebGL GIS Map canvas.
- **Backend API**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0.
- **Data & GIS**: Shapely 2.1, GeoPandas, NumPy 2.5, SQLite/Spatialite, PostgreSQL + PostGIS support.
- **AI & Orchestration**: Google ADK, Google GenAI SDK (`gemini-2.5-flash`), 17 typed tools, Bounded Iteration Loop.
- **Security & Guardrails**: PBKDF2-HMAC-SHA256 password hashing, PyJWT, Prompt Injection Defense, Output Claim Validator.
- **Deployment**: Docker, Docker Compose, Google Cloud Run specifications.

---

## 4. 10 Toggleable GIS Layers

1. ☑ **Cyclone Track**: Historical path and projected trajectory line.
2. ☑ **Forecast Cone**: Dynamic uncertainty swath expanding with forecast lead time.
3. ☑ **Wind Field**: 120km radius gale force wind swath.
4. ☑ **Rainfall Accumulation**: Surface precipitation accumulation.
5. ☑ **Storm Surge Inundation**: Coastal sea intrusion boundary based on bathymetric slope.
6. ☑ **Flood Risk**: Topographic low-elevation retention polygons.
7. ☑ **Road Network (45 Segments)**: Passable vs flooded corridors with flood depth in cm.
8. ☑ **Hospitals (12 Facilities)**: Capacity, ICU, generator reserves, direct accessibility state.
9. ☑ **Cyclone Shelters (8 Hubs)**: High-perch evacuation centers with capacity checks.
10. ☑ **Power Grid (15 Substations)**: Low-elevation transmission and distribution assets.

---

## 5. Quickstart & Local Setup

### Backend Setup
```bash
# 1. Navigate to backend directory
cd cyclone-sentinel-ai/backend

# 2. Configure environment
cp .env.example .env

# 3. Seed demo data (Cyclone DEMO-01, 12 hospitals, 45 roads, 8 shelters, 15 power nodes)
python app/database/seed_demo.py

# 4. Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
FastAPI interactive Swagger documentation available at: `http://localhost:8000/docs`

### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd cyclone-sentinel-ai/frontend

# 2. Install dependencies
npm install

# 3. Start Next.js development server
npm run dev
```
Open command center at: `http://localhost:3000`

---

## 6. Running All Tests

```bash
cd cyclone-sentinel-ai
$env:PYTHONPATH="backend"
python -m pytest backend/tests/ -v
```

All 29 tests pass covering:
- Deterministic Risk Engine (`Hazard * Exposure * Vulnerability` and weighted models)
- Storm Surge parametric calculations (SLOSH inverse barometer + shelf shoaling)
- Hydrologic rainfall runoff and road/facility flood blockage
- Context Engineering 5-layer assembly and spatial bounding
- 17 typed supervisor agent tools
- Bounded loop iteration cap (max 5 iterations)
- Prompt injection defense & LLM claim verification
- Human-in-the-loop advisory approval & SHA-256 audit log chaining
- REST API endpoint contracts

---

## 7. Operational & Scientific Disclaimer

> **MODELLED SCENARIO DECISION SUPPORT — NOT AN OFFICIAL FORECAST**  
> This platform is an anticipatory decision-support prototype. It does not replace statutory forecasts issued by national meteorological organizations (e.g. IMD, JTWC, WMO). Consequential operational directives (evacuation orders, infrastructure de-energization) strictly require authorized human commander approval.
