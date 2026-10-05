"""
Generate 500 synthetic training records for the packaging recommendation ML model.

Output: ml/dataset/training_data.csv

Reproducible — uses numpy random seed 42.
Run from any directory; file paths are resolved relative to this script's location.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

# ── Resolve project root and add ml/ to sys.path ─────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_SCRIPT_DIR)          # ml/
_PROJECT_ROOT = os.path.dirname(_ML_DIR)        # project root

if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)

# ── Output path ───────────────────────────────────────────────────────────────
OUTPUT_CSV = os.path.join(_SCRIPT_DIR, "training_data.csv")

# ── Food categories ───────────────────────────────────────────────────────────
FOOD_CATEGORIES = [
    "fruits", "vegetables", "cereals", "pulses", "spices",
    "dairy", "meat", "fish", "bakery", "snacks",
    "processed_food", "beverages", "other",
]
CATEGORY_TO_INT = {cat: idx for idx, cat in enumerate(FOOD_CATEGORIES)}

# ── Material codes (must match knowledge base) ────────────────────────────────
ALL_MATERIAL_CODES = [
    "LDPE", "HDPE", "PP", "BOPP", "PET",
    "MET-PET", "ALU-FOIL", "EVOH", "PAPERBOARD", "KRAFT",
    "GLASS", "PET-BOTTLE", "HDPE-BOTTLE", "PLA", "BIO-FILM",
    "PA", "PERF-LDPE", "BOPP-PE", "MET-PET-PE", "RETORT-POUCH",
    "VACUUM-PA-PE", "MAP-FILM", "MULTILAYER-PE-PA", "PVC",
]

# ── Category → plausible best materials (for label generation) ───────────────
_CATEGORY_MATERIAL_MAP: dict[str, list[str]] = {
    "fruits":        ["PERF-LDPE", "PLA", "LDPE", "MAP-FILM", "BIO-FILM"],
    "vegetables":    ["PERF-LDPE", "LDPE", "PLA", "MAP-FILM", "BIO-FILM"],
    "cereals":       ["BOPP-PE", "BOPP", "HDPE", "MET-PET-PE", "KRAFT"],
    "pulses":        ["BOPP-PE", "BOPP", "HDPE", "MET-PET-PE", "PA"],
    "spices":        ["MET-PET", "ALU-FOIL", "MET-PET-PE", "GLASS", "PET"],
    "dairy":         ["HDPE-BOTTLE", "PET-BOTTLE", "EVOH", "PA", "VACUUM-PA-PE"],
    "meat":          ["VACUUM-PA-PE", "MAP-FILM", "RETORT-POUCH", "PA", "MULTILAYER-PE-PA"],
    "fish":          ["VACUUM-PA-PE", "MAP-FILM", "RETORT-POUCH", "PA", "MULTILAYER-PE-PA"],
    "bakery":        ["BOPP", "PP", "LDPE", "PLA", "BOPP-PE"],
    "snacks":        ["MET-PET-PE", "MET-PET", "BOPP", "BOPP-PE", "ALU-FOIL"],
    "processed_food":["RETORT-POUCH", "EVOH", "PET", "PA", "MET-PET-PE"],
    "beverages":     ["PET-BOTTLE", "HDPE-BOTTLE", "GLASS", "PET", "HDPE"],
    "other":         ["KRAFT", "PAPERBOARD", "LDPE", "PET", "BOPP"],
}

# ── Priority codes ────────────────────────────────────────────────────────────
PRIORITY_CODES = ["low_cost", "max_shelf_life", "food_safety", "sustainability", "balanced"]
PRIORITY_TO_INT = {p: i for i, p in enumerate(PRIORITY_CODES)}


def _sensitivity_int(rng: np.random.Generator, p_high: float = 0.3) -> int:
    """Return 0 (low), 1 (medium), or 2 (high) with weighted probability."""
    return rng.choice([0, 1, 2], p=[0.4, 0.3, p_high])


def generate(n_samples: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    rows = []
    for _ in range(n_samples):
        # Food category
        category = rng.choice(FOOD_CATEGORIES)
        cat_int = CATEGORY_TO_INT[category]

        # Composition
        moisture_content = float(rng.uniform(5, 90))
        ph = float(rng.uniform(3.0, 8.0))
        fat_content = float(rng.uniform(0, 50))
        water_activity = float(rng.uniform(0.1, 0.99))
        respiration_rate = float(rng.uniform(0, 200))

        # Sensitivities (0=low, 1=medium, 2=high)
        oxygen_sensitivity = int(_sensitivity_int(rng))
        moisture_sensitivity = int(_sensitivity_int(rng))
        light_sensitivity = int(_sensitivity_int(rng))

        # Storage
        storage_temp = float(rng.uniform(-5, 40))
        storage_duration_days = int(rng.integers(1, 365))
        required_shelf_life_days = int(rng.integers(1, 730))
        budget_index = float(rng.uniform(0.1, 1.0))

        # Priority
        priority_encoded = int(rng.choice(len(PRIORITY_CODES)))

        # ── Label: best_material_code ─────────────────────────────────
        # Deterministic assignment: score each candidate with simple heuristic
        plausible_materials = _CATEGORY_MATERIAL_MAP.get(category, ALL_MATERIAL_CODES)

        # Add some noise by occasionally picking from all materials
        if rng.uniform() < 0.15:
            plausible_materials = ALL_MATERIAL_CODES

        # Simple heuristic score for label generation
        best_code, best_heuristic = _select_best(
            plausible_materials,
            oxygen_sensitivity, moisture_sensitivity, light_sensitivity,
            storage_temp, required_shelf_life_days, budget_index, priority_encoded, rng,
        )

        # Clamp overall_score to 0-100
        overall_score = float(np.clip(best_heuristic, 0.0, 100.0))

        rows.append({
            "food_category": cat_int,
            "moisture_content": round(moisture_content, 2),
            "ph": round(ph, 2),
            "fat_content": round(fat_content, 2),
            "water_activity": round(water_activity, 3),
            "respiration_rate": round(respiration_rate, 2),
            "oxygen_sensitivity": oxygen_sensitivity,
            "moisture_sensitivity": moisture_sensitivity,
            "light_sensitivity": light_sensitivity,
            "storage_temp": round(storage_temp, 1),
            "storage_duration_days": storage_duration_days,
            "required_shelf_life_days": required_shelf_life_days,
            "budget_index": round(budget_index, 3),
            "priority_encoded": priority_encoded,
            "best_material_code": best_code,
            "overall_score": round(overall_score, 2),
        })

    return pd.DataFrame(rows)


# ── Minimal in-process barrier knowledge for label scoring ───────────────────
_KB: dict[str, dict[str, float]] = {
    "LDPE":            {"o2": 0.30, "moist": 0.75, "light": 0.20, "therm": 0.35, "cost": 0.25, "slm": 1.1},
    "HDPE":            {"o2": 0.35, "moist": 0.85, "light": 0.25, "therm": 0.50, "cost": 0.30, "slm": 1.2},
    "PP":              {"o2": 0.40, "moist": 0.80, "light": 0.20, "therm": 0.65, "cost": 0.30, "slm": 1.15},
    "BOPP":            {"o2": 0.42, "moist": 0.82, "light": 0.22, "therm": 0.55, "cost": 0.35, "slm": 1.2},
    "PET":             {"o2": 0.60, "moist": 0.78, "light": 0.20, "therm": 0.60, "cost": 0.40, "slm": 1.3},
    "MET-PET":         {"o2": 0.90, "moist": 0.92, "light": 0.95, "therm": 0.60, "cost": 0.55, "slm": 1.8},
    "ALU-FOIL":        {"o2": 0.99, "moist": 0.99, "light": 1.00, "therm": 0.85, "cost": 0.65, "slm": 2.0},
    "EVOH":            {"o2": 0.97, "moist": 0.60, "light": 0.30, "therm": 0.55, "cost": 0.70, "slm": 2.5},
    "PAPERBOARD":      {"o2": 0.25, "moist": 0.30, "light": 0.60, "therm": 0.30, "cost": 0.30, "slm": 1.0},
    "KRAFT":           {"o2": 0.15, "moist": 0.20, "light": 0.55, "therm": 0.20, "cost": 0.20, "slm": 0.9},
    "GLASS":           {"o2": 1.00, "moist": 1.00, "light": 0.50, "therm": 0.70, "cost": 0.70, "slm": 2.0},
    "PET-BOTTLE":      {"o2": 0.62, "moist": 0.80, "light": 0.20, "therm": 0.58, "cost": 0.42, "slm": 1.4},
    "HDPE-BOTTLE":     {"o2": 0.38, "moist": 0.87, "light": 0.30, "therm": 0.52, "cost": 0.33, "slm": 1.3},
    "PLA":             {"o2": 0.50, "moist": 0.55, "light": 0.20, "therm": 0.30, "cost": 0.60, "slm": 1.0},
    "BIO-FILM":        {"o2": 0.45, "moist": 0.50, "light": 0.20, "therm": 0.25, "cost": 0.65, "slm": 0.95},
    "PA":              {"o2": 0.70, "moist": 0.55, "light": 0.20, "therm": 0.75, "cost": 0.55, "slm": 1.5},
    "PERF-LDPE":       {"o2": 0.10, "moist": 0.40, "light": 0.10, "therm": 0.35, "cost": 0.20, "slm": 1.05},
    "BOPP-PE":         {"o2": 0.45, "moist": 0.85, "light": 0.25, "therm": 0.55, "cost": 0.40, "slm": 1.35},
    "MET-PET-PE":      {"o2": 0.91, "moist": 0.93, "light": 0.96, "therm": 0.60, "cost": 0.58, "slm": 2.0},
    "RETORT-POUCH":    {"o2": 0.99, "moist": 0.99, "light": 1.00, "therm": 0.90, "cost": 0.80, "slm": 3.0},
    "VACUUM-PA-PE":    {"o2": 0.80, "moist": 0.88, "light": 0.22, "therm": 0.70, "cost": 0.55, "slm": 2.2},
    "MAP-FILM":        {"o2": 0.72, "moist": 0.75, "light": 0.25, "therm": 0.55, "cost": 0.60, "slm": 2.0},
    "MULTILAYER-PE-PA":{"o2": 0.78, "moist": 0.86, "light": 0.22, "therm": 0.68, "cost": 0.52, "slm": 1.9},
    "PVC":             {"o2": 0.50, "moist": 0.65, "light": 0.15, "therm": 0.45, "cost": 0.30, "slm": 1.0},
}

_SENS_REQUIRED = {0: 0.30, 1: 0.60, 2: 0.90}
_PRIORITY_WEIGHTS_LIST = [
    # low_cost
    {"o2": 0.08, "moist": 0.08, "light": 0.05, "therm": 0.05, "cost": 0.25, "sl": 0.14},
    # max_shelf_life
    {"o2": 0.12, "moist": 0.10, "light": 0.08, "therm": 0.06, "cost": 0.10, "sl": 0.25},
    # food_safety
    {"o2": 0.12, "moist": 0.10, "light": 0.08, "therm": 0.05, "cost": 0.10, "sl": 0.15},
    # sustainability
    {"o2": 0.08, "moist": 0.08, "light": 0.06, "therm": 0.05, "cost": 0.10, "sl": 0.10},
    # balanced
    {"o2": 0.10, "moist": 0.10, "light": 0.08, "therm": 0.08, "cost": 0.14, "sl": 0.14},
]


def _heuristic_score(
    code: str,
    o2_sens: int,
    moist_sens: int,
    light_sens: int,
    storage_temp: float,
    required_shelf_life_days: int,
    budget_index: float,
    priority_idx: int,
) -> float:
    kb = _KB.get(code)
    if kb is None:
        return 0.0
    w = _PRIORITY_WEIGHTS_LIST[priority_idx]
    req_o2 = _SENS_REQUIRED[o2_sens]
    req_moist = _SENS_REQUIRED[moist_sens]
    req_light = _SENS_REQUIRED[light_sens]

    s_o2 = min(kb["o2"] / req_o2, 1.0) * 100 if req_o2 > 0 else 100.0
    s_moist = min(kb["moist"] / req_moist, 1.0) * 100 if req_moist > 0 else 100.0
    s_light = min(kb["light"] / req_light, 1.0) * 100 if req_light > 0 else 100.0
    s_therm = min(kb["therm"] / 0.60, 1.0) * 100 if storage_temp > 30 else kb["therm"] * 100

    # Cost score: lower cost_index → higher cost score; adjusted by budget
    cost_adj = max(0.0, 1.0 - kb["cost"] / max(budget_index, 0.1))
    s_cost = min(cost_adj, 1.0) * 100

    # Shelf life score
    perishability_baseline = 30.0
    achieved = perishability_baseline * kb["slm"]
    s_sl = min(achieved / max(required_shelf_life_days, 1), 1.0) * 100

    score = (
        w["o2"] * s_o2
        + w["moist"] * s_moist
        + w["light"] * s_light
        + w["therm"] * s_therm
        + w["cost"] * s_cost
        + w["sl"] * s_sl
    )
    return float(score)


def _select_best(
    candidates: list[str],
    o2: int, moist: int, light: int,
    storage_temp: float, req_shelf: int, budget: float,
    priority_idx: int,
    rng: np.random.Generator,
) -> tuple[str, float]:
    scores = {
        c: _heuristic_score(c, o2, moist, light, storage_temp, req_shelf, budget, priority_idx)
        for c in candidates
    }
    # Add tiny deterministic jitter to break exact ties consistently
    best = max(scores, key=lambda c: (scores[c], c))
    return best, scores[best]


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df = generate(n_samples=500, seed=42)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_CSV}")
    print(df.head())
    print(f"\nMaterial distribution:\n{df['best_material_code'].value_counts()}")
