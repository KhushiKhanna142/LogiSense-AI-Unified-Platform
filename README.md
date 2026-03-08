# LogiSense AI Unified Platform 🚀

**An End-to-End AI Logistics OS combining Predictive Analytics (F1-F4), the Zen Platform (ZenDec, ZenRTO, ZenETA), and Advanced LangGraph Intelligence (F8-F10).**

## 🌐 Platform Architecture

The LogiSense Unified Platform operates via a synchronized Next.js frontend and a monolithic FastAPI backend serving multiple intelligent sub-agents that communicate over Redis and LangGraph.

| Module | Core Functionality | AI / ML Tech Stack |
|--------|--------------------|--------------------|
| **Observer (F1/F4)** | Real-time Anomaly Detection & Warehouse Load Polling | Isolation Forest, ARIMA(1,1,1) |
| **Reasoner (F2)** | Supply Chain Contagion Risk Analysis & Cascade Trees | Directed Acyclic Graph (DAG) BFS, LightGBM |
| **Actor (F3/F4)** | Autonomous Carrier Subbing, Rerouting & Intake Staggering | Kolmogorov–Smirnov Drift, Heuristics |
| **ZenDec (F6)** | Route & Carrier Decision Engine | TOPSIS optimization, AQI APIs, LLM Stress Test |
| **ZenRTO (F6)** | RTO Fraud Detection & Risk Scoring | LightGBM, SHAP, Twilio Connect |
| **ZenETA (F7)** | ETA Quantile Pediction | XGBoost (p50/p90/p99) |
| **F8 Explainability** | Actionable Transparency & Counterfactual Reasoning | SHAP Heatmaps, Risk Matrices, Plotly JS |
| **F9 Blockchain** | Auditable Logistics Ledger & Decision Immutability | Polygon-compatible Web3.py, Merkle Trees |
| **F10 Synthesis** | Decentralized Agentic Control Loop | LangGraph, Chat LLM State |

## 🏗️ Repository Structure

```
LogiSense/
├── backend/
│   ├── agents/            # Legacy F1-F4 Agents (Observer, Reasoner, Actor)
│   ├── api/               # Unified FastAPI App (main.py router)
│   ├── features/          # New Intelligence Models
│   │   ├── explainability/ # F8 SHAP Heatmaps
│   │   ├── blockchain/     # F9 Auditing
│   │   └── synthesis/      # F10 LangGraph
│   ├── zen/               # The Zen Platform
│   │   ├── core/          # TOPSIS & Autonomy pipelines
│   │   ├── routers/       # Demand, ETA, RTO modular routers
│   │   └── services/      # Gemini, AQI, Waybills
│   ├── db/                # Supabase ORM layer
│   └── streams/           # Redis real-time Pub/Sub
│
└── frontend/
    └── src/
        ├── App.jsx        # Unified Tabbed Dashboard Router
        ├── components/
        │   ├── features/  # F8 SHAP Plotly Components
        │   ├── zen/       # IFrames and React Components for Zen
        │   └── ...        # Legacy React Components (Warehouse Map, Anomaly Badge)
```

## 🚀 Quick Start Guide

### 1. Requirements
Ensure you have Python 3.9+ and Node.js v18+.

### 2. Environment Variables
Copy `.env.example` to `backend/.env` and insert your Supabase and LLM API keys.

### 3. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Start the Unified API Server
```bash
# Export PYTHONPATH so feature modules resolve correctly 
PYTHONPATH=. python3 -m uvicorn api.main:app --reload --port 8000
```
API Documentation will be live at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Start the React/Vite Dashboard
Open a second terminal window:
```bash
cd frontend
npm install
npm run dev
```
Dashboard will be live at: [http://localhost:5173](http://localhost:5173)

---
*Built with React, FastAPI, LightGBM, XGBoost, and LangGraph.*
