"""
Packaging recommendation feature preprocessor.

Numerical features → StandardScaler.
Categorical features → OneHotEncoder(handle_unknown='ignore').

Saves the fitted pipeline to ml/models/preprocessor.pkl via joblib.
"""
from __future__ import annotations

import os
import sys
import logging

logger = logging.getLogger(__name__)

# ── Resolve paths ─────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_SCRIPT_DIR)
_MODELS_DIR = os.path.join(_ML_DIR, "models")

if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)

# ── Feature specification (must match synthetic_data.py columns) ──────────────
NUMERICAL_FEATURES: list[str] = [
    "moisture_content",
    "ph",
    "fat_content",
    "water_activity",
    "respiration_rate",
    "storage_temp",
    "storage_duration_days",
    "required_shelf_life_days",
    "budget_index",
]

CATEGORICAL_FEATURES: list[str] = [
    "food_category",
    "oxygen_sensitivity",
    "moisture_sensitivity",
    "light_sensitivity",
    "priority_encoded",
]

ALL_FEATURES: list[str] = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


class PackagingPreprocessor:
    """
    Sklearn Pipeline wrapper for feature preprocessing.

    fit_transform(X) and transform(X) accept a pandas DataFrame or
    a list of dicts with the columns defined in ALL_FEATURES.
    """

    def __init__(self) -> None:
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler

        self.pipeline: Pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    ColumnTransformer(
                        transformers=[
                            ("num", StandardScaler(), NUMERICAL_FEATURES),
                            (
                                "cat",
                                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                                CATEGORICAL_FEATURES,
                            ),
                        ],
                        remainder="drop",
                    ),
                )
            ]
        )
        self._fitted = False

    # ------------------------------------------------------------------
    def fit_transform(self, X):  # type: ignore[no-untyped-def]
        import pandas as pd

        df = pd.DataFrame(X) if not hasattr(X, "columns") else X
        df = df[ALL_FEATURES]
        result = self.pipeline.fit_transform(df)
        self._fitted = True
        return result

    def transform(self, X):  # type: ignore[no-untyped-def]
        import pandas as pd

        if not self._fitted:
            raise RuntimeError("Preprocessor has not been fitted yet. Call fit_transform first.")
        df = pd.DataFrame(X) if not hasattr(X, "columns") else X
        df = df[ALL_FEATURES]
        return self.pipeline.transform(df)

    def save(self, path: str | None = None) -> str:
        """Save the fitted pipeline. Returns the save path."""
        import joblib

        if path is None:
            os.makedirs(_MODELS_DIR, exist_ok=True)
            path = os.path.join(_MODELS_DIR, "preprocessor.pkl")
        joblib.dump(self.pipeline, path)
        logger.info("Preprocessor saved to %s", path)
        return path

    @classmethod
    def load(cls, path: str | None = None) -> "PackagingPreprocessor":
        """Load a previously fitted pipeline from disk."""
        import joblib

        if path is None:
            path = os.path.join(_MODELS_DIR, "preprocessor.pkl")
        instance = cls.__new__(cls)
        instance.pipeline = joblib.load(path)
        instance._fitted = True
        logger.info("Preprocessor loaded from %s", path)
        return instance
