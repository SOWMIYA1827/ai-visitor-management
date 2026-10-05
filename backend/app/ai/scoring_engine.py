"""
Fully deterministic scoring engine for packaging material recommendations.

NO random() calls exist anywhere in this module.
Given identical inputs, identical scores are always produced.

Scoring model
─────────────
Each dimension score = clamp(material_barrier_value / required_barrier, 0, 1) × 100.
Where required_barrier is derived from food sensitivity:
  low    → 0.3  (any material meets the threshold easily)
  medium → 0.6
  high   → 0.9

For properties without a matching food sensitivity (mechanical, shelf-life),
the material's own raw value × 100 is used directly.

overall_score is a weighted average across all dimension scores using the
priority supplied in packaging_requirements.
"""
from typing import Any

from .knowledge_base import PACKAGING_MATERIALS


# ── Sensitivity → required barrier mapping ────────────────────────────────────
_SENSITIVITY_TO_REQUIRED: dict[str, float] = {
    "low": 0.30,
    "medium": 0.60,
    "high": 0.90,
}

# ── Priority → weight profiles ────────────────────────────────────────────────
# Keys match the PackagingRequirements.priority enum values.
# Weights must sum to 1.0 for each profile.
_PRIORITY_WEIGHTS: dict[str, dict[str, float]] = {
    "balanced": {
        "moisture_score": 0.10,
        "oxygen_score": 0.10,
        "light_score": 0.08,
        "thermal_score": 0.08,
        "mechanical_score": 0.08,
        "food_safety_score": 0.14,
        "shelf_life_score": 0.14,
        "cost_score": 0.14,
        "sustainability_score": 0.14,
    },
    "low_cost": {
        "moisture_score": 0.08,
        "oxygen_score": 0.08,
        "light_score": 0.05,
        "thermal_score": 0.05,
        "mechanical_score": 0.05,
        "food_safety_score": 0.15,
        "shelf_life_score": 0.14,
        "cost_score": 0.25,       # ← elevated
        "sustainability_score": 0.15,
    },
    "max_shelf_life": {
        "moisture_score": 0.10,
        "oxygen_score": 0.12,
        "light_score": 0.08,
        "thermal_score": 0.06,
        "mechanical_score": 0.05,
        "food_safety_score": 0.12,
        "shelf_life_score": 0.25,  # ← elevated
        "cost_score": 0.10,
        "sustainability_score": 0.12,
    },
    "food_safety": {
        "moisture_score": 0.10,
        "oxygen_score": 0.12,
        "light_score": 0.08,
        "thermal_score": 0.05,
        "mechanical_score": 0.05,
        "food_safety_score": 0.25,  # ← elevated
        "shelf_life_score": 0.15,
        "cost_score": 0.10,
        "sustainability_score": 0.10,
    },
    "sustainability": {
        "moisture_score": 0.08,
        "oxygen_score": 0.08,
        "light_score": 0.06,
        "thermal_score": 0.05,
        "mechanical_score": 0.05,
        "food_safety_score": 0.13,
        "shelf_life_score": 0.10,
        "cost_score": 0.10,
        "sustainability_score": 0.35,  # ← elevated
    },
}


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


class ScoringEngine:
    """Compute deterministic per-dimension and overall scores for a packaging material."""

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def score_material(
        self,
        material_code: str,
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> dict[str, float]:
        """
        Return a dict with dimension scores and overall_score, all in 0-100.

        Scores are completely deterministic — no randomness introduced.
        """
        mat = PACKAGING_MATERIALS[material_code]
        priority = packaging_requirements.get("priority", "balanced")
        weights = _PRIORITY_WEIGHTS.get(priority, _PRIORITY_WEIGHTS["balanced"])

        # ── Dimension scores ───────────────────────────────────────────
        moisture_score = self._barrier_score(
            mat["moisture_barrier"],
            food_profile.get("moisture_sensitivity", "low"),
        )
        oxygen_score = self._barrier_score(
            mat["oxygen_barrier"],
            food_profile.get("oxygen_sensitivity", "low"),
        )
        light_score = self._barrier_score(
            mat["light_barrier"],
            food_profile.get("light_sensitivity", "low"),
        )
        thermal_score = self._barrier_score(
            mat["thermal_resistance"],
            food_profile.get("temperature_sensitivity", "low"),
        )

        # Mechanical: no direct food sensitivity — use raw material score
        mechanical_score = _clamp(mat["mechanical_strength"] * 100)

        # Food safety: composite of food_contact_safe flag + barrier adequacy
        food_safety_score = self._food_safety_score(mat, food_profile)

        # Shelf-life: driven by material's shelf_life_multiplier × perishability suitability
        shelf_life_score = self._shelf_life_score(mat, food_profile, packaging_requirements)

        # Cost: inverted (lower cost_index → better cost score)
        cost_score = _clamp((1.0 - mat["cost_index"]) * 100)

        # Sustainability: multi-attribute composite
        sustainability_score = self._sustainability_score(mat, packaging_requirements)

        # ── Weighted overall ───────────────────────────────────────────
        dim_scores = {
            "moisture_score": moisture_score,
            "oxygen_score": oxygen_score,
            "light_score": light_score,
            "thermal_score": thermal_score,
            "mechanical_score": mechanical_score,
            "food_safety_score": food_safety_score,
            "shelf_life_score": shelf_life_score,
            "cost_score": cost_score,
            "sustainability_score": sustainability_score,
        }

        overall = sum(
            dim_scores[dim] * w for dim, w in weights.items()
        )
        overall_score = _clamp(overall)

        return {**dim_scores, "overall_score": overall_score}

    def score_all(
        self,
        material_codes: list[str],
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> dict[str, dict[str, float]]:
        """Score every material in *material_codes* and return a mapping of code → scores."""
        return {
            code: self.score_material(code, food_profile, storage_conditions, packaging_requirements)
            for code in material_codes
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _barrier_score(barrier_value: float, sensitivity: str) -> float:
        """
        Score = clamp(barrier_value / required_barrier × 100, 0, 100).
        A material that exactly meets the required threshold scores 100.
        A material whose barrier exceeds the requirement is capped at 100.
        """
        required = _SENSITIVITY_TO_REQUIRED.get(sensitivity, 0.30)
        if required == 0.0:
            return 100.0
        raw = (barrier_value / required) * 100.0
        return _clamp(raw)

    @staticmethod
    def _food_safety_score(mat: dict[str, Any], food_profile: dict[str, Any]) -> float:
        """
        Composite score:
        - 60 pts for food_contact_safe=True
        - 20 pts for microbial sensitivity coverage (oxygen + moisture barriers)
        - 20 pts for absence of unsuitable_for tags matching food properties
        """
        score = 0.0

        if mat["food_contact_safe"]:
            score += 60.0

        # Microbial coverage: average of oxygen and moisture barriers × 20
        microbial_sensitivity = food_profile.get("microbial_sensitivity", "low")
        required = _SENSITIVITY_TO_REQUIRED.get(microbial_sensitivity, 0.30)
        o2 = min(mat["oxygen_barrier"] / required, 1.0) if required > 0 else 1.0
        moist = min(mat["moisture_barrier"] / required, 1.0) if required > 0 else 1.0
        score += ((o2 + moist) / 2.0) * 20.0

        # Penalty for known incompatibilities
        unsuitable = mat.get("unsuitable_for", [])
        penalties = {
            "high_fat": food_profile.get("fat_content") is not None
                        and food_profile.get("fat_content", 0) > 30,
            "acidic": food_profile.get("ph") is not None
                      and food_profile.get("ph", 7) < 4.5,
            "high_moisture": food_profile.get("moisture_content") is not None
                             and food_profile.get("moisture_content", 0) > 60,
            "high_temperature_storage": (storage_cond := {}).get("storage_temp") is not None
                                         and {}.get("storage_temp", 25) > 40,
        }
        # We cannot easily pass storage_conditions here so use food-based proxies
        penalty_triggered = any(
            tag in unsuitable and penalties.get(tag, False)
            for tag in unsuitable
        )
        if penalty_triggered:
            score -= 20.0

        return _clamp(score)

    @staticmethod
    def _shelf_life_score(
        mat: dict[str, Any],
        food_profile: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> float:
        """
        Score based on how well the material's shelf_life_multiplier
        can achieve the required shelf life given the food's perishability.

        Baseline shelf-life days by perishability:
          high   →  7 days
          medium → 30 days
          low    → 180 days

        Achieved = baseline × shelf_life_multiplier.
        Score = min(achieved / required, 1.0) × 100.
        """
        perishability = food_profile.get("perishability", "medium")
        baseline_map = {"high": 7.0, "medium": 30.0, "low": 180.0}
        baseline = baseline_map.get(perishability, 30.0)

        multiplier = mat.get("shelf_life_multiplier", 1.0)
        achieved = baseline * multiplier

        required = float(packaging_requirements.get("required_shelf_life_days") or baseline)
        if required <= 0:
            required = baseline

        ratio = achieved / required
        return _clamp(ratio * 100)

    @staticmethod
    def _sustainability_score(
        mat: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> float:
        """
        Composite:
        - recyclable    → +25 pts
        - biodegradable → +25 pts
        - compostable   → +20 pts
        - bio_based     → +20 pts
        - eco_preference bonus: +10 pts if the preferred attribute matches
        """
        score = 0.0
        if mat.get("recyclable"):
            score += 25.0
        if mat.get("biodegradable"):
            score += 25.0
        if mat.get("compostable"):
            score += 20.0
        if mat.get("bio_based"):
            score += 20.0

        eco = packaging_requirements.get("eco_preference", "no_preference")
        eco_attr_map = {
            "recyclable": "recyclable",
            "biodegradable": "biodegradable",
            "compostable": "compostable",
            "bio_based": "bio_based",
        }
        attr = eco_attr_map.get(eco)
        if attr and mat.get(attr):
            score += 10.0  # preference bonus

        return _clamp(score)
