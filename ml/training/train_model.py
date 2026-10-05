"""
Train the packaging recommendation ML models.

Models trained:
  1. RandomForestRegressor  → predicts overall_score
  2. RandomForestClassifier → predicts best_material_code

Both models and the preprocessor are saved to ml/models/.

Usage:
  cd ml && python training/train_model.py
  OR run from project root:
  python ml/training/train_model.py
"""
from __future__ import annotations

import os
import sys

# ── Resolve paths ─────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_SCRIPT_DIR)          # ml/
_MODELS_DIR = os.path.join(_ML_DIR, "models")
_DATASET_DIR = os.path.join(_ML_DIR, "dataset")
_TRAINING_CSV = os.path.join(_DATASET_DIR, "training_data.csv")

# Ensure ml/ is in sys.path so sibling packages can be imported
if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)


def main() -> None:
    import joblib
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.metrics import accuracy_score, mean_absolute_error
    from sklearn.model_selection import train_test_split

    from preprocessing.preprocessor import PackagingPreprocessor

    # ── 1. Generate dataset if missing ────────────────────────────────────────
    if not os.path.exists(_TRAINING_CSV):
        print("training_data.csv not found — generating synthetic dataset …")
        # Import via path manipulation (dataset/ is a sibling sub-package)
        from dataset.synthetic_data import generate, OUTPUT_CSV
        os.makedirs(_DATASET_DIR, exist_ok=True)
        df_gen = generate(n_samples=500, seed=42)
        df_gen.to_csv(OUTPUT_CSV, index=False)
        print(f"  → Saved {len(df_gen)} rows to {OUTPUT_CSV}")

    # ── 2. Load dataset ────────────────────────────────────────────────────────
    df = pd.read_csv(_TRAINING_CSV)
    print(f"Loaded {len(df)} training records from {_TRAINING_CSV}")

    # ── 3. Feature / target split ──────────────────────────────────────────────
    from preprocessing.preprocessor import ALL_FEATURES

    X = df[ALL_FEATURES]
    y_score = df["overall_score"].values.astype(np.float64)
    y_material = df["best_material_code"].values

    # ── 4. Train/test split (80/20, seed=42) ──────────────────────────────────
    X_train, X_test, y_score_train, y_score_test, y_mat_train, y_mat_test = train_test_split(
        X, y_score, y_material, test_size=0.20, random_state=42
    )

    # ── 5. Fit preprocessor ────────────────────────────────────────────────────
    preprocessor = PackagingPreprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # ── 6. Train regression model (overall_score) ──────────────────────────────
    print("Training RandomForestRegressor (overall_score) …")
    reg_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    reg_model.fit(X_train_transformed, y_score_train)
    y_score_pred = reg_model.predict(X_test_transformed)
    mae = mean_absolute_error(y_score_test, y_score_pred)
    print(f"  Regressor MAE on hold-out: {mae:.4f}")

    # ── 7. Train classifier model (best_material_code) ────────────────────────
    print("Training RandomForestClassifier (best_material_code) …")
    clf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf_model.fit(X_train_transformed, y_mat_train)
    y_mat_pred = clf_model.predict(X_test_transformed)
    acc = accuracy_score(y_mat_test, y_mat_pred)
    print(f"  Classifier accuracy on hold-out: {acc:.4f}")

    # ── 8. Save models and preprocessor ───────────────────────────────────────
    os.makedirs(_MODELS_DIR, exist_ok=True)

    # Main packaged model file (classifier) — named packaging_model.pkl
    # as specified in acceptance criteria
    clf_path = os.path.join(_MODELS_DIR, "packaging_model.pkl")
    joblib.dump(clf_model, clf_path)
    print(f"  Classifier saved → {clf_path}")

    # Regressor
    reg_path = os.path.join(_MODELS_DIR, "score_model.pkl")
    joblib.dump(reg_model, reg_path)
    print(f"  Regressor saved  → {reg_path}")

    # Preprocessor
    preprocessor.save()
    print(f"  Preprocessor saved → {os.path.join(_MODELS_DIR, 'preprocessor.pkl')}")

    print("\nTraining complete. Models saved.")


if __name__ == "__main__":
    main()
