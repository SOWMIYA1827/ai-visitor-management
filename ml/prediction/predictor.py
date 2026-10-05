"""
ML predictor for packaging recommendation.

Loads the trained classifier (packaging_model.pkl) and preprocessor
(preprocessor.pkl) from ml/models/ and exposes a predict() method.

Gracefully handles missing model files by logging a warning and returning
a low-confidence result so the rule+scoring engine takes precedence.
"""
from __future__ import annotations

import logging
import os
import sys

logger = logging.getLogger(__name__)

# ── Resolve paths ─────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_SCRIPT_DIR)
_MODELS_DIR = os.path.join(_ML_DIR, "models")
_MODEL_PATH = os.path.join(_MODELS_DIR, "packaging_model.pkl")
_PREPROCESSOR_PATH = os.path.join(_MODELS_DIR, "preprocessor.pkl")

if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)


class PackagingPredictor:
    """
    Wraps the trained RandomForestClassifier to predict the best packaging
    material code for a set of input features.

    Usage:
        predictor = PackagingPredictor()
        result = predictor.predict({
            "food_category": 2,
            "moisture_content": 12.5,
            ...
        })
        # {"predicted_material_code": "BOPP-PE", "confidence_score": 0.85}
    """

    def __init__(self) -> None:
        self._model = None
        self._preprocessor_pipeline = None
        self._loaded = False
        self._load()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def predict(self, features: dict) -> dict:
        """
        Predict the best material code for *features*.

        Parameters
        ----------
        features : dict
            Flat dict with keys matching the training feature columns
            (see ml/preprocessing/preprocessor.py ALL_FEATURES).

        Returns
        -------
        dict
            {"predicted_material_code": str, "confidence_score": float}
        """
        if not self._loaded:
            logger.warning("ML models not loaded; returning low-confidence fallback.")
            return {"predicted_material_code": "BOPP-PE", "confidence_score": 0.0}

        try:
            import pandas as pd
            from preprocessing.preprocessor import ALL_FEATURES

            # Build a single-row DataFrame
            row = {col: features.get(col, 0) for col in ALL_FEATURES}
            df = pd.DataFrame([row])

            # Transform
            X = self._preprocessor_pipeline.transform(df)

            # Predict class probabilities
            proba = self._model.predict_proba(X)[0]
            predicted_idx = int(proba.argmax())
            predicted_code: str = self._model.classes_[predicted_idx]
            confidence: float = float(proba[predicted_idx])

            return {
                "predicted_material_code": predicted_code,
                "confidence_score": confidence,
            }
        except Exception as exc:  # noqa: BLE001
            logger.warning("Prediction failed (%s); returning low-confidence fallback.", exc)
            return {"predicted_material_code": "BOPP-PE", "confidence_score": 0.0}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Load models from disk. Logs warning and sets _loaded=False on failure."""
        try:
            import joblib

            if not os.path.exists(_MODEL_PATH):
                logger.warning(
                    "packaging_model.pkl not found at %s. "
                    "Run ml/training/train_model.py first.",
                    _MODEL_PATH,
                )
                return

            if not os.path.exists(_PREPROCESSOR_PATH):
                logger.warning(
                    "preprocessor.pkl not found at %s. "
                    "Run ml/training/train_model.py first.",
                    _PREPROCESSOR_PATH,
                )
                return

            self._model = joblib.load(_MODEL_PATH)
            self._preprocessor_pipeline = joblib.load(_PREPROCESSOR_PATH)
            self._loaded = True
            logger.info("ML models loaded successfully from %s", _MODELS_DIR)

        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load ML models: %s", exc)
            self._loaded = False
