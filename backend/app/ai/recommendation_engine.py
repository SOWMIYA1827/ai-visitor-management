"""
Unified recommendation engine.

Combines:
  - RuleEngine      : deterministic candidate filtering
  - ScoringEngine   : deterministic multi-dimension scoring
  - Explainer       : human-readable explanation + risk factors
  - PackagingPredictor (optional ML override at confidence > 0.80)

Entry point: RecommendationEngine.recommend(food_profile, storage_conditions,
             packaging_requirements) -> RecommendationResult
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from .explainer import Explainer
from .knowledge_base import PACKAGING_MATERIALS
from .rule_engine import RuleEngine
from .scoring_engine import ScoringEngine

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Result dataclass — fields match the Recommendation ORM model exactly
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class RecommendationResult:
    # Identifiers for ORM linkage
    primary_material_code: str
    alternative_material_codes: list[str]

    # Recommendation output
    packaging_structure: str
    barrier_properties: dict[str, Any]
    recommended_thickness_um: float

    # Storage guidance
    storage_conditions_recommended: str

    # Shelf life
    shelf_life_min_days: int
    shelf_life_max_days: int

    # Quality / risk
    risk_factors: list[str]

    # Scores (0-100)
    sustainability_score: float
    cost_score: float
    food_safety_score: float
    overall_score: float

    # Explanation text
    explanation: str

    # Full per-material scores for all candidates (used by frontend charts)
    all_scores: dict[str, dict[str, float]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict suitable for constructing an ORM Recommendation row."""
        return {
            "primary_material_code": self.primary_material_code,
            "alternative_material_codes": self.alternative_material_codes,
            "packaging_structure": self.packaging_structure,
            "barrier_properties": self.barrier_properties,
            "recommended_thickness_um": self.recommended_thickness_um,
            "storage_conditions_recommended": self.storage_conditions_recommended,
            "shelf_life_min_days": self.shelf_life_min_days,
            "shelf_life_max_days": self.shelf_life_max_days,
            "risk_factors": self.risk_factors,
            "sustainability_score": self.sustainability_score,
            "cost_score": self.cost_score,
            "food_safety_score": self.food_safety_score,
            "overall_score": self.overall_score,
            "explanation": self.explanation,
            "all_scores": self.all_scores,
        }


# ──────────────────────────────────────────────────────────────────────────────
# Perishability → baseline shelf-life days
# ──────────────────────────────────────────────────────────────────────────────
_PERISHABILITY_BASELINE: dict[str, tuple[int, int]] = {
    "high":   (3, 7),
    "medium": (14, 30),
    "low":    (90, 180),
}

_CATEGORY_STORAGE_NOTES: dict[str, str] = {
    "fruits": "Store at 2-8°C with relative humidity 90-95%.",
    "vegetables": "Store at 0-5°C with relative humidity 90-95%.",
    "cereals": "Store in cool, dry conditions at 15-25°C and <65% RH.",
    "pulses": "Store at ambient temperature, away from moisture and pests.",
    "spices": "Store in airtight packaging away from light, heat, and moisture.",
    "dairy": "Maintain cold chain at 2-6°C; ensure hermetic seal.",
    "meat": "Maintain strict cold chain at 0-4°C; monitor oxygen levels.",
    "fish": "Store at 0-2°C or frozen at -18°C; vacuum or MAP packaging recommended.",
    "bakery": "Store at ambient temperature in moisture-proof packaging.",
    "snacks": "Store at ambient temperature away from direct sunlight.",
    "processed_food": "Follow product-specific temperature and humidity guidelines.",
    "beverages": "Store upright in cool conditions; protect from UV light.",
    "other": "Store according to product-specific requirements.",
}


# ──────────────────────────────────────────────────────────────────────────────
# Main engine
# ──────────────────────────────────────────────────────────────────────────────

class RecommendationEngine:
    """
    Single entry point for generating a packaging recommendation.

    All sub-components (rule engine, scoring engine, explainer) are
    instantiated once at construction time and reused across calls.
    """

    def __init__(self) -> None:
        self._rule_engine = RuleEngine()
        self._scoring_engine = ScoringEngine()
        self._explainer = Explainer()
        self._predictor: Any = None  # lazy-loaded ML predictor

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def recommend(
        self,
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> RecommendationResult:
        """
        Generate a packaging recommendation.

        Parameters
        ----------
        food_profile : dict
            Keys match FoodProfile ORM / FoodProfileCreate schema fields.
        storage_conditions : dict
            Keys match StorageConditions ORM / StorageConditionsInput schema.
        packaging_requirements : dict
            Keys match PackagingRequirements ORM / PackagingRequirementsInput schema.

        Returns
        -------
        RecommendationResult
            Fully populated dataclass. Scores are 0-100 floats.
        """
        # 1. Filter candidates
        candidates = self._rule_engine.filter_candidates(
            food_profile, storage_conditions, packaging_requirements
        )
        logger.debug("Candidates after rule filtering: %s", candidates)

        # 2. Score each candidate
        all_scores = self._scoring_engine.score_all(
            candidates, food_profile, storage_conditions, packaging_requirements
        )

        # 3. Sort by overall_score descending (deterministic: tie-break by material_code)
        ranked = sorted(
            candidates,
            key=lambda c: (-all_scores[c]["overall_score"], c),
        )

        # 4. Optional ML override (confidence > 0.8 bumps that material to #1)
        ranked = self._apply_ml_override(ranked, all_scores, food_profile, storage_conditions, packaging_requirements)

        # 5. Primary + alternatives
        primary_code = ranked[0]
        alternative_codes = ranked[1:4]  # up to 3 alternatives

        primary_scores = all_scores[primary_code]

        # 6. Packaging structure string
        packaging_structure = self._build_packaging_structure(
            primary_code, packaging_requirements
        )

        # 7. Barrier properties dict
        barrier_properties = self._build_barrier_properties(primary_code)

        # 8. Recommended thickness
        recommended_thickness_um = self._recommended_thickness(
            primary_code, packaging_requirements
        )

        # 9. Shelf life
        shelf_life_min, shelf_life_max = self._compute_shelf_life(
            primary_code, food_profile, packaging_requirements
        )

        # 10. Storage recommendation
        storage_recommended = self._storage_recommendation(
            food_profile, storage_conditions
        )

        # 11. Explanation + risk factors
        explanation = self._explainer.generate_explanation(
            primary_code,
            primary_scores,
            food_profile,
            storage_conditions,
            packaging_requirements,
        )
        risk_factors = self._explainer.generate_risk_factors(
            primary_code, food_profile, storage_conditions
        )

        return RecommendationResult(
            primary_material_code=primary_code,
            alternative_material_codes=alternative_codes,
            packaging_structure=packaging_structure,
            barrier_properties=barrier_properties,
            recommended_thickness_um=recommended_thickness_um,
            storage_conditions_recommended=storage_recommended,
            shelf_life_min_days=shelf_life_min,
            shelf_life_max_days=shelf_life_max,
            risk_factors=risk_factors,
            sustainability_score=round(primary_scores["sustainability_score"], 2),
            cost_score=round(primary_scores["cost_score"], 2),
            food_safety_score=round(primary_scores["food_safety_score"], 2),
            overall_score=round(primary_scores["overall_score"], 2),
            explanation=explanation,
            all_scores=all_scores,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _apply_ml_override(
        self,
        ranked: list[str],
        all_scores: dict[str, dict[str, float]],
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> list[str]:
        """
        Optionally load the ML predictor and let a high-confidence prediction
        influence the top recommendation.

        The rule+scoring engine always provides the fallback. ML override only
        applies when confidence > 0.80 AND the predicted code is in the candidate set.
        """
        if self._predictor is None:
            self._predictor = self._load_predictor()

        if self._predictor is None:
            return ranked  # ML models not available

        try:
            features = self._build_ml_features(food_profile, storage_conditions, packaging_requirements)
            result = self._predictor.predict(features)
            predicted_code = result.get("predicted_material_code")
            confidence = result.get("confidence_score", 0.0)

            if confidence > 0.80 and predicted_code in all_scores:
                # Move predicted_code to front if not already
                if ranked[0] != predicted_code:
                    logger.info(
                        "ML override: %s (confidence=%.2f) promoted to #1",
                        predicted_code, confidence
                    )
                    ranked = [predicted_code] + [c for c in ranked if c != predicted_code]
        except Exception as exc:  # noqa: BLE001
            logger.warning("ML predictor failed (%s); using rule+scoring engine.", exc)

        return ranked

    @staticmethod
    def _load_predictor() -> Any | None:
        """Lazily import PackagingPredictor to avoid hard dependency on ML libs."""
        try:
            import sys
            import os
            # Add ml/ directory to path so predictor can import its siblings
            ml_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml")
            ml_dir = os.path.abspath(ml_dir)
            if ml_dir not in sys.path:
                sys.path.insert(0, ml_dir)
            from prediction.predictor import PackagingPredictor  # type: ignore[import]
            return PackagingPredictor()
        except Exception as exc:  # noqa: BLE001
            logger.debug("PackagingPredictor not available: %s", exc)
            return None

    @staticmethod
    def _build_ml_features(
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> dict[str, Any]:
        """Convert domain dicts into the flat feature dict expected by the ML model."""
        category_map = {
            "fruits": 0, "vegetables": 1, "cereals": 2, "pulses": 3,
            "spices": 4, "dairy": 5, "meat": 6, "fish": 7,
            "bakery": 8, "snacks": 9, "processed_food": 10,
            "beverages": 11, "other": 12,
        }
        sensitivity_map = {"low": 0, "medium": 1, "high": 2}
        priority_map = {
            "low_cost": 0, "max_shelf_life": 1, "food_safety": 2,
            "sustainability": 3, "balanced": 4,
        }

        return {
            "food_category": category_map.get(food_profile.get("category", "other"), 12),
            "moisture_content": food_profile.get("moisture_content") or 10.0,
            "ph": food_profile.get("ph") or 6.5,
            "fat_content": food_profile.get("fat_content") or 5.0,
            "water_activity": food_profile.get("water_activity") or 0.6,
            "respiration_rate": food_profile.get("respiration_rate") or 5.0,
            "oxygen_sensitivity": sensitivity_map.get(
                food_profile.get("oxygen_sensitivity", "low"), 0
            ),
            "moisture_sensitivity": sensitivity_map.get(
                food_profile.get("moisture_sensitivity", "low"), 0
            ),
            "light_sensitivity": sensitivity_map.get(
                food_profile.get("light_sensitivity", "low"), 0
            ),
            "storage_temp": storage_conditions.get("storage_temp") or 25.0,
            "storage_duration_days": storage_conditions.get("storage_duration_days") or 30,
            "required_shelf_life_days": packaging_requirements.get("required_shelf_life_days") or 30,
            "budget_index": min(
                (packaging_requirements.get("budget") or 500) / 5000.0, 1.0
            ),
            "priority_encoded": priority_map.get(
                packaging_requirements.get("priority", "balanced"), 4
            ),
        }

    @staticmethod
    def _build_packaging_structure(
        material_code: str,
        packaging_requirements: dict[str, Any],
    ) -> str:
        """Build a human-readable packaging structure string."""
        mat = PACKAGING_MATERIALS[material_code]
        thickness_mid = (
            mat["typical_thickness_min_um"] + mat["typical_thickness_max_um"]
        ) / 2.0

        pkg_type = packaging_requirements.get("packaging_type") or "flexible"

        # Use mid-range thickness for the label
        return f"{pkg_type.replace('_', ' ').title()} — {mat['name']} {thickness_mid:.0f} µm"

    @staticmethod
    def _build_barrier_properties(material_code: str) -> dict[str, Any]:
        """Extract barrier scores as a labelled dict for display."""
        mat = PACKAGING_MATERIALS[material_code]
        return {
            "moisture_barrier": mat["moisture_barrier"],
            "oxygen_barrier": mat["oxygen_barrier"],
            "light_barrier": mat["light_barrier"],
            "thermal_resistance": mat["thermal_resistance"],
            "mechanical_strength": mat["mechanical_strength"],
        }

    @staticmethod
    def _recommended_thickness(
        material_code: str,
        packaging_requirements: dict[str, Any],
    ) -> float:
        """
        Choose a recommended thickness based on required shelf life.
        Higher shelf life → thicker film (upper quartile of range).
        """
        mat = PACKAGING_MATERIALS[material_code]
        lo = mat["typical_thickness_min_um"]
        hi = mat["typical_thickness_max_um"]

        req_days = packaging_requirements.get("required_shelf_life_days") or 30
        if req_days <= 14:
            # Short shelf life: use lower third
            return lo + (hi - lo) * 0.25
        elif req_days <= 90:
            # Medium: midpoint
            return (lo + hi) / 2.0
        else:
            # Long shelf life: upper third
            return lo + (hi - lo) * 0.80

    @staticmethod
    def _compute_shelf_life(
        material_code: str,
        food_profile: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> tuple[int, int]:
        """Estimate achievable shelf-life range (min, max) in days."""
        mat = PACKAGING_MATERIALS[material_code]
        perishability = food_profile.get("perishability", "medium")

        base_min, base_max = _PERISHABILITY_BASELINE.get(perishability, (14, 30))
        multiplier = mat.get("shelf_life_multiplier", 1.0)

        achieved_min = max(1, int(base_min * multiplier))
        achieved_max = max(achieved_min + 1, int(base_max * multiplier))

        return achieved_min, achieved_max

    @staticmethod
    def _storage_recommendation(
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
    ) -> str:
        """Return a storage guidance string based on food category and conditions."""
        category = food_profile.get("category", "other")
        base_note = _CATEGORY_STORAGE_NOTES.get(category, _CATEGORY_STORAGE_NOTES["other"])

        cold_chain = storage_conditions.get("cold_chain_required", False)
        transport = storage_conditions.get("transportation_type")

        extras = []
        if cold_chain:
            extras.append("Cold chain must be maintained throughout distribution.")
        if transport == "air":
            extras.append(
                "Air transport: ensure pressure-stable packaging to prevent seal failure."
            )
        elif transport == "sea":
            extras.append(
                "Sea freight: use moisture-absorbing desiccants in outer cartons."
            )

        return " ".join([base_note] + extras)
