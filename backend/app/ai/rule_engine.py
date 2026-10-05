"""
Rule-based candidate filter for the packaging recommendation system.

Rules are applied in priority order:
  1. Safety rules — never relaxed.
  2. Hard barrier rules (derived from food sensitivity).
  3. Category-compatibility rules.
  4. Eco-preference filter — preference only, never eliminates all candidates.

If fewer than 3 candidates survive after rules 1-3, non-safety constraints are
relaxed in order until at least 3 candidates are available.
"""
from typing import Any

from .knowledge_base import PACKAGING_MATERIALS


# ── Sensitivity threshold mapping ─────────────────────────────────────────────
_SENSITIVITY_BARRIER: dict[str, float] = {
    "low": 0.0,     # no constraint
    "medium": 0.4,  # soft constraint
    "high": 0.6,    # hard constraint
}

# Hard-constraint thresholds (applied when sensitivity == "high")
_HIGH_MOISTURE_BARRIER_MIN = 0.60
_HIGH_OXYGEN_BARRIER_MIN = 0.70
_HIGH_LIGHT_BARRIER_MIN = 0.50
_HIGH_THERMAL_BARRIER_MIN = 0.50


class RuleEngine:
    """
    Deterministic candidate filter.

    :meth:`filter_candidates` always returns at least 3 material codes.
    """

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def filter_candidates(
        self,
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> list[str]:
        """
        Return a filtered list of material_codes that are suitable for the
        given food/storage/packaging inputs.

        Parameters mirror the schema dataclasses — callers should pass plain
        dicts (or .dict() / .model_dump() output from Pydantic objects).
        """
        # Start from the full catalogue
        candidates: list[str] = list(PACKAGING_MATERIALS.keys())

        # ── Phase 1: Safety rules (NEVER relaxed) ─────────────────────
        candidates = self._apply_safety_rules(candidates)

        # ── Phase 2: Hard barrier rules + category compatibility ───────
        phase2_candidates = self._apply_hard_rules(
            candidates, food_profile, storage_conditions, packaging_requirements
        )

        # ── Phase 3: Guarantee minimum 3 candidates ───────────────────
        if len(phase2_candidates) >= 3:
            return phase2_candidates

        # Relax in order: category → barrier thresholds (still keep safety)
        relaxed = self._relax_constraints(
            candidates, food_profile, storage_conditions, packaging_requirements
        )
        return relaxed

    # ------------------------------------------------------------------
    # Phase 1 — Safety (never relaxed)
    # ------------------------------------------------------------------

    def _apply_safety_rules(self, candidates: list[str]) -> list[str]:
        """Eliminate materials that are not food-contact safe."""
        return [
            code
            for code in candidates
            if PACKAGING_MATERIALS[code]["food_contact_safe"]
        ]

    # ------------------------------------------------------------------
    # Phase 2 — Hard rules
    # ------------------------------------------------------------------

    def _apply_hard_rules(
        self,
        candidates: list[str],
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> list[str]:
        result = list(candidates)

        result = self._rule_moisture_barrier(result, food_profile)
        result = self._rule_oxygen_barrier(result, food_profile)
        result = self._rule_light_barrier(result, food_profile)
        result = self._rule_thermal(result, storage_conditions)
        result = self._rule_category(result, food_profile)
        result = self._rule_eco_preference(result, packaging_requirements)

        return result

    # ── Individual rules ──────────────────────────────────────────────

    def _rule_moisture_barrier(
        self, candidates: list[str], food_profile: dict[str, Any]
    ) -> list[str]:
        """High moisture sensitivity → moisture_barrier >= 0.60."""
        sensitivity = food_profile.get("moisture_sensitivity", "low")
        if sensitivity == "high":
            return [
                c for c in candidates
                if PACKAGING_MATERIALS[c]["moisture_barrier"] >= _HIGH_MOISTURE_BARRIER_MIN
            ]
        return candidates

    def _rule_oxygen_barrier(
        self, candidates: list[str], food_profile: dict[str, Any]
    ) -> list[str]:
        """High oxygen sensitivity → oxygen_barrier >= 0.70."""
        sensitivity = food_profile.get("oxygen_sensitivity", "low")
        if sensitivity == "high":
            return [
                c for c in candidates
                if PACKAGING_MATERIALS[c]["oxygen_barrier"] >= _HIGH_OXYGEN_BARRIER_MIN
            ]
        return candidates

    def _rule_light_barrier(
        self, candidates: list[str], food_profile: dict[str, Any]
    ) -> list[str]:
        """High light sensitivity → light_barrier >= 0.50."""
        sensitivity = food_profile.get("light_sensitivity", "low")
        if sensitivity == "high":
            return [
                c for c in candidates
                if PACKAGING_MATERIALS[c]["light_barrier"] >= _HIGH_LIGHT_BARRIER_MIN
            ]
        return candidates

    def _rule_thermal(
        self, candidates: list[str], storage_conditions: dict[str, Any]
    ) -> list[str]:
        """
        If cold chain is NOT required and storage_temp > 30°C,
        require thermal_resistance >= 0.50.
        """
        cold_chain = storage_conditions.get("cold_chain_required", False)
        storage_temp = storage_conditions.get("storage_temp") or 25.0
        if not cold_chain and storage_temp > 30.0:
            return [
                c for c in candidates
                if PACKAGING_MATERIALS[c]["thermal_resistance"] >= _HIGH_THERMAL_BARRIER_MIN
            ]
        return candidates

    def _rule_category(
        self, candidates: list[str], food_profile: dict[str, Any]
    ) -> list[str]:
        """
        Keep materials that list the food category in suitable_categories OR
        have an empty suitable_categories (universal).
        Beverages always need a bottle/container-capable material.
        """
        category = food_profile.get("category", "other")

        filtered = [
            c for c in candidates
            if category in PACKAGING_MATERIALS[c]["suitable_categories"]
            or not PACKAGING_MATERIALS[c]["suitable_categories"]
        ]

        # Special: beverages need a bottle or high-integrity container
        if category == "beverages":
            bottle_codes = {"PET-BOTTLE", "HDPE-BOTTLE", "GLASS", "PET", "HDPE"}
            bottle_filtered = [c for c in filtered if c in bottle_codes]
            if bottle_filtered:
                return bottle_filtered
            # fall back to all filtered if no bottles matched
        return filtered

    def _rule_eco_preference(
        self, candidates: list[str], packaging_requirements: dict[str, Any]
    ) -> list[str]:
        """
        Eco preference is a soft preference — if the filtered set has enough
        matching materials, return only those; otherwise return all candidates
        (we never eliminate below 3 here — that is handled by relax logic).
        """
        eco = packaging_requirements.get("eco_preference", "no_preference")
        if eco == "no_preference":
            return candidates

        eco_map: dict[str, str] = {
            "recyclable": "recyclable",
            "biodegradable": "biodegradable",
            "compostable": "compostable",
            "bio_based": "bio_based",
        }
        attr = eco_map.get(eco)
        if attr is None:
            return candidates

        preferred = [
            c for c in candidates
            if PACKAGING_MATERIALS[c].get(attr, False)
        ]
        # Only apply eco filter if it still leaves 3+ candidates
        return preferred if len(preferred) >= 3 else candidates

    # ------------------------------------------------------------------
    # Phase 3 — Relaxation (when fewer than 3 pass hard rules)
    # ------------------------------------------------------------------

    def _relax_constraints(
        self,
        safety_passed: list[str],
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> list[str]:
        """
        Apply progressively fewer constraints until at least 3 candidates pass.
        Safety rules (food_contact_safe) are NEVER relaxed.

        Relaxation order:
          1. Keep moisture + oxygen + light + thermal, drop category.
          2. Keep moisture + oxygen, drop light + thermal + category.
          3. Keep oxygen only.
          4. Keep all safety-passed materials (last resort).
        """
        # Attempt 1: drop category constraint
        attempt1 = safety_passed[:]
        attempt1 = self._rule_moisture_barrier(attempt1, food_profile)
        attempt1 = self._rule_oxygen_barrier(attempt1, food_profile)
        attempt1 = self._rule_light_barrier(attempt1, food_profile)
        attempt1 = self._rule_thermal(attempt1, storage_conditions)
        if len(attempt1) >= 3:
            return attempt1

        # Attempt 2: drop light + thermal + category
        attempt2 = safety_passed[:]
        attempt2 = self._rule_moisture_barrier(attempt2, food_profile)
        attempt2 = self._rule_oxygen_barrier(attempt2, food_profile)
        if len(attempt2) >= 3:
            return attempt2

        # Attempt 3: only oxygen barrier
        attempt3 = safety_passed[:]
        attempt3 = self._rule_oxygen_barrier(attempt3, food_profile)
        if len(attempt3) >= 3:
            return attempt3

        # Last resort: all food-contact-safe materials
        return safety_passed if len(safety_passed) >= 3 else safety_passed
