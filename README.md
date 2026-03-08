# LogiSense AI 🚢

> **Cyber Cypher 5.0 · Advanced Track**  
> A real-time multi-agent AI system for predictive logistics and supply chain disruption management.

---

## Features

### F1 — Anomaly Detection (Observer Agent)
The Observer Agent polls every active shipment every 5 minutes from Supabase, applying 4 rule-based checks and an Isolation Forest model to flag anomalies:

| Rule | Trigger | Severity |
|---|---|---|
| ETA Drift | `eta_current > eta_original × 1.2` | HIGH |
| Carrier Silence | No check-in in past 20 min | CRITICAL |
| Status Stall | Status unchanged for >6 hrs | MEDIUM |
| Warehouse Load | Warehouse >85% capacity | HIGH |

Anomalies are published to a **Redis Stream** (`reasoner_queue`) and broadcast live to the dashboard via **WebSocket**.

---

### F2 — Cascade Risk Tree (Reasoner Agent)
The Reasoner Agent subscribes to anomaly events and runs BFS on a pre-loaded directed dependency graph of 1000 shipments:

- **BFS traversal** finds all downstream shipments at risk from a single failure
- **LightGBM scoring** rates each node's delay probability using ETA, carrier reliability, and warehouse load
- Publishes a **CascadeTree** (nodes + edges) to the dashboard as a D3 force-directed graph
- Trees with **20–40 nodes** are common when a critical carrier fails

---

### F3 — Carrier Swap (Actor Agent)
The Actor Agent monitors for repeated low-reliability carriers using a **Kolmogorov–Smirnov drift test** on historical on-time rates:

- KS stat > 0.7 and p-value < 0.05 → carrier flagged
- Best replacement selected by highest reliability score from non-blacklisted carriers
- All affected `IN_TRANSIT` shipments reassigned in Supabase
- Decision logged with **SHA-256 fingerprint** for F9 blockchain audit
- Swap event broadcast live to dashboard swap log

---

### F4 — Warehouse Congestion Predictor (Observer + Actor)
Three-tier warehouse monitoring system with automatic rerouting:

| Trigger | Condition | Action |
|---|---|---|
| Load Threshold | `current_load_pct >= 85%` | REDIRECT → lowest-load alternate |
| Throughput Drop | >20% drop vs 15-min rolling avg | STAGGER intake by 15 min batches |
| ARIMA Pre-emptive | forecast hits 85% within 2 hrs | Pre-emptive stagger at 70% load |

- Observer syncs warehouse loads from Supabase → Redis every poll cycle
- **Leaflet map** shows all 4 warehouse nodes (Mumbai, Delhi, Bangalore, Pune) colour-coded by load
- WH-02 turns red and redirects shipments to WH-04 during the demo

---

## Project Structure

```
LogiSense/
├── backend/
│   ├── agents/
│   │   ├── observer/          # F1 anomaly detection + F4 warehouse monitor
│   │   │   └── warehouse/     # monitor.py, forecaster.py, publisher.py
│   │   ├── reasoner/          # F2 BFS cascade tree + LightGBM scoring
│   │   └── actor/             # F3 carrier swap + F4 redirect/stagger tools
│   ├── api/
│   │   ├── main.py            # FastAPI app + WebSocket + REST endpoints
│   │   └── websocket.py       # WebSocket connection manager
│   ├── db/
│   │   └── supabase_client.py # All Supabase query functions
│   ├── streams/
│   │   └── redis_client.py    # Redis Streams + cache helpers
│   ├── scripts/
│   │   ├── demo_seed.py       # Full F1→F4 demo data injector
│   │   ├── generate_dag.py    # Shipment dependency graph seeder
│   │   └── generate_warehouses.py
│   └── requirements.txt
└── frontend/
    └── src/components/
        ├── AnomalyBadge.jsx   # F1 live anomaly feed
        ├── CascadeTree.jsx    # F2 D3 force-directed graph
        ├── SwapNotification.jsx  # F3 carrier swap log
        └── WarehouseHeatmap.jsx  # F4 Leaflet map
```

---

## Quick Start

### 1. Clone & configure
```bash
git clone https://github.com/KhushiKhanna142/LogiSense.git
cd LogiSense
cp .env.example backend/.env   # fill in your keys
```

### 2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install frontend dependencies
```bash
cd frontend
npm install
```

### 4. Seed the database
```sql
-- Run in Supabase SQL editor:
-- backend/scripts/add_f4_tables.sql
```
```bash
cd backend
PYTHONPATH=. python3 scripts/generate_dag.py
PYTHONPATH=. python3 scripts/generate_warehouses.py
```

### 5. Start backend
```bash
cd backend
PYTHONPATH=. python3 -m uvicorn api.main:app --reload --port 8000
```

### 6. Start frontend
```bash
cd frontend
npm run dev
# → http://localhost:5173
```

### 7. Trigger the demo
```bash
cd backend
PYTHONPATH=. python3 scripts/demo_seed.py
```

Watch the dashboard: anomaly feed, cascade tree, carrier swap log, and warehouse heatmap all update within 30 seconds.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python · FastAPI · Uvicorn |
| AI/ML | Isolation Forest · LightGBM · ARIMA(1,1,1) · KS-test |
| Database | Supabase (PostgreSQL) |
| Cache / Streams | Redis (Redis Streams) |
| Frontend | React · Vite · D3.js · Leaflet · TailwindCSS |
| Scheduling | APScheduler |

---

## Environment Variables

See `.env.example` for required keys.
