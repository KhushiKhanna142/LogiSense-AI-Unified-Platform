from __future__ import annotations
"""
mock_ml_node.py — Simulates the ML Prediction Agent (Feature 5) output.

PURPOSE:
  Lets you run and test Feature 8 completely standalone,
  without needing Feature 5 to be built yet.
  Also serves as the exact contract that Feature 5 MUST follow.

USAGE:
  from feature_8.mocks.mock_ml_node import run_mock_ml_prediction
  state = run_mock_ml_prediction(n_children=60)
  # Now pass state into explainability_node(state)

CONTRACT FOR FEATURE 5 TEAM:
  Your ML prediction node must write these exact keys to GraphState:
    - state["model"]       → trained sklearn-compatible model
    - state["X_df"]        → pd.DataFrame, same shape used for .predict()
    - state["predictions"] → list of dicts: [{child_id, risk_score, ...}]
    - state["feature_names"] → list of column name strings
"""

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from typing import Any


def generate_synthetic_shipments(n: int = 60, seed: int = 42) -> pd.DataFrame:
    """
    Generates a synthetic dataset matching the expected Logistics feature schema.
    """
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "eta_delay_minutes":   rng.integers(0, 120, n),
        "carrier_reliability": rng.integers(50, 100, n),
        "weather_risk_index":  rng.integers(0, 10, n),
        "route_congestion":    rng.integers(0, 100, n),
        "border_delay":        rng.integers(0, 2, n),
        "fragile_cargo":       rng.integers(0, 2, n),
        "priority_level":      rng.integers(1, 5, n),
        "historical_loss":     rng.integers(0, 3, n),
    })


def train_mock_model(X: pd.DataFrame, y: pd.Series) -> Any:
    """Trains a quick XGBoost classifier. Feature 5 should replace this with their real model."""
    model = XGBClassifier(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
        verbosity=0,
    )
    model.fit(X, y)
    return model


def run_mock_ml_prediction(n_shipments: int = 60) -> dict:
    """
    Returns a GraphState-compatible dict as if Feature 5 had run.
    """
    X = generate_synthetic_shipments(n_shipments)
    y = (X["eta_delay_minutes"] > 45).astype(int)
    model = train_mock_model(X, y)

    probs = model.predict_proba(X)[:, 1]
    predictions = [
        {
            "shipment_id": f"SHP{i:03d}",
            "risk_score": float(round(p * 100, 2)),
            "risk_label": _risk_label(p * 100),
        }
        for i, p in enumerate(probs)
    ]

    return {
        "model": model,
        "X_df": X,
        "predictions": predictions,
        "feature_names": list(X.columns),
        "raw_data": X.to_dict(orient="records"),
        "query": None,
        "error": None,
        "current_node": "ml_prediction",
        # Feature 8 output keys — not yet populated
        "shap_heatmap_json": None,
        "shap_matrix_json": None,
        "shap_waterfall_json": None,
        "top_features": None,
        "shap_values_raw": None,
    }


def _risk_label(score: float) -> str:
    if score < 25:   return "LOW"
    if score < 50:   return "MEDIUM"
    if score < 70:   return "HIGH"
    return "CRITICAL"
