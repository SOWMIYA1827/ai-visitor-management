"""
Human-readable explanation generator for packaging recommendations.

Produces a 3-5 sentence explanation of WHY a particular material was
recommended, plus a list of concrete risk factors.
"""
from typing import Any

from .knowledge_base import PACKAGING_MATERIALS


# ── Mapping from score dimension names to readable labels ─────────────────────
_DIM_LABELS: dict[str, str] = {
    "moisture_score": "moisture barrier",
    "oxygen_score": "oxygen barrier",
    "light_score": "light barrier",
    "thermal_score": "thermal resistance",
    "mechanical_score": "mechanical strength",
    "food_safety_score": "food safety compliance",
    "shelf_life_score": "shelf-life suitability",
    "cost_score": "cost efficiency",
    "sustainability_score": "sustainability",
}

_SENSITIVITY_LABELS: dict[str, str] = {
    "moisture_sensitivity": "moisture",
    "oxygen_sensitivity": "oxygen",
    "light_sensitivity": "light",
    "temperature_sensitivity": "temperature",
    "odor_sensitivity": "odor",
    "microbial_sensitivity": "microbial contamination",
}

_PERISHABILITY_LABELS: dict[str, str] = {
    "high": "highly perishable",
    "medium": "moderately perishable",
    "low": "shelf-stable",
}


class Explainer:
    """Generate natural-language explanations and risk factor lists."""

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_explanation(
        self,
        primary_material_code: str,
        scores: dict[str, float],
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
        packaging_requirements: dict[str, Any],
    ) -> str:
        """
        Return a 3-5 sentence explanation of why *primary_material_code* was
        selected for the given food/storage/packaging context.
        """
        mat = PACKAGING_MATERIALS[primary_material_code]
        food_name = food_profile.get("food_name", "the food product")
        category = food_profile.get("category", "food product")
        perishability = food_profile.get("perishability", "medium")

        # Top 2 scoring dimensions (excluding overall_score)
        dim_scores = {k: v for k, v in scores.items() if k != "overall_score"}
        top_dims = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)[:2]
        top_dim_labels = [_DIM_LABELS.get(d, d) for d, _ in top_dims]

        # Key sensitivities (medium or high)
        key_sensitivities = []
        for attr, label in _SENSITIVITY_LABELS.items():
            level = food_profile.get(attr, "low")
            if level in ("medium", "high"):
                key_sensitivities.append(f"{level} {label} sensitivity")

        # Shelf life context
        shelf_life_min = packaging_requirements.get("required_shelf_life_days")
        storage_dur = storage_conditions.get("storage_duration_days")
        shelf_life_context = (
            f"a required shelf life of {shelf_life_min} days"
            if shelf_life_min
            else f"a storage duration of {storage_dur} days"
            if storage_dur
            else "the intended storage duration"
        )

        # Sustainability note
        eco_flags = []
        if mat.get("recyclable"):
            eco_flags.append("recyclable")
        if mat.get("biodegradable"):
            eco_flags.append("biodegradable")
        if mat.get("compostable"):
            eco_flags.append("compostable")
        if mat.get("bio_based"):
            eco_flags.append("bio-based")
        sustainability_note = (
            f"From a sustainability standpoint, {mat['name']} is {', '.join(eco_flags)}."
            if eco_flags
            else f"{mat['name']} is not inherently recyclable or biodegradable, "
                 "so proper disposal practices are advised."
        )

        # Build sentences
        perishability_label = _PERISHABILITY_LABELS.get(perishability, "moderately perishable")
        sensitivity_clause = (
            f" It specifically addresses the product's {' and '.join(key_sensitivities[:2])}."
            if key_sensitivities
            else ""
        )

        overall = scores.get("overall_score", 0.0)
        sentence1 = (
            f"{mat['name']} was selected as the primary packaging material for {food_name} "
            f"with an overall recommendation score of {overall:.1f}/100."
        )
        sentence2 = (
            f"It ranked highest in {top_dim_labels[0]} and {top_dim_labels[1]}, "
            f"making it well-suited for this {perishability_label} {category} product."
        )
        sentence3 = sentence2  # placeholder overridden below
        sentence3 = (
            f"This material is designed to handle {shelf_life_context}, "
            f"providing reliable protection throughout the supply chain."
            + sensitivity_clause
        )
        sentence4 = sustainability_note
        sentence5 = (
            f"Typical application thickness ranges from "
            f"{mat['typical_thickness_min_um']:.0f} µm to "
            f"{mat['typical_thickness_max_um']:.0f} µm, "
            f"which balances material cost against barrier performance."
        )

        return " ".join([sentence1, sentence2, sentence3, sentence4, sentence5])

    def generate_risk_factors(
        self,
        material_code: str,
        food_profile: dict[str, Any],
        storage_conditions: dict[str, Any],
    ) -> list[str]:
        """
        Return 2-4 concrete risk statements for the chosen material.

        Risks are determined deterministically from material properties
        and food/storage inputs.
        """
        mat = PACKAGING_MATERIALS[material_code]
        risks: list[str] = []

        # Risk: low oxygen barrier + high oxygen sensitivity
        if (
            food_profile.get("oxygen_sensitivity") == "high"
            and mat["oxygen_barrier"] < 0.70
        ):
            risks.append(
                f"{mat['name']} has an oxygen barrier of {mat['oxygen_barrier']:.2f}; "
                "for highly oxygen-sensitive products, consider adding an EVOH or aluminium layer."
            )

        # Risk: low moisture barrier + high moisture sensitivity
        if (
            food_profile.get("moisture_sensitivity") == "high"
            and mat["moisture_barrier"] < 0.60
        ):
            risks.append(
                f"{mat['name']} may not provide adequate moisture protection "
                "(barrier score {:.2f}); evaluate desiccant sachets or secondary packaging.".format(
                    mat["moisture_barrier"]
                )
            )

        # Risk: light barrier insufficient for light-sensitive food
        if (
            food_profile.get("light_sensitivity") == "high"
            and mat["light_barrier"] < 0.50
        ):
            risks.append(
                f"The light barrier of {mat['name']} ({mat['light_barrier']:.2f}) is low; "
                "store in opaque outer cartons or use amber/dark pigmented packaging."
            )

        # Risk: high storage temperature + low thermal resistance
        storage_temp = storage_conditions.get("storage_temp") or 25.0
        if storage_temp > 35.0 and mat["thermal_resistance"] < 0.50:
            risks.append(
                f"Storage at {storage_temp:.0f}°C may exceed the thermal tolerance of "
                f"{mat['name']} (resistance score {mat['thermal_resistance']:.2f}); "
                "ensure climate-controlled storage."
            )

        # Risk: fat content + paper-based material
        fat_content = food_profile.get("fat_content") or 0.0
        if fat_content > 20.0 and mat.get("material_code") in {"PAPERBOARD", "KRAFT"}:
            risks.append(
                "High fat content (>20%) may cause grease migration through paper-based packaging; "
                "use grease-proof coatings or a plastic inner liner."
            )

        # Risk: acidic food + aluminium foil (bare)
        ph = food_profile.get("ph")
        if ph is not None and ph < 4.5 and material_code == "ALU-FOIL":
            risks.append(
                f"Bare aluminium foil may corrode in contact with acidic foods (pH {ph:.1f}); "
                "use lacquer-coated foil or a PET/foil laminate."
            )

        # Risk: non-recyclable material with sustainability priority
        eco = {}
        if not mat.get("recyclable") and not mat.get("biodegradable"):
            risks.append(
                f"{mat['name']} is neither recyclable nor biodegradable; "
                "proper waste management or EPR (Extended Producer Responsibility) compliance is required."
            )

        # Cap at 4 risks, ensure at least 2 (add generic if needed)
        if len(risks) < 2:
            risks.append(
                "Ensure packaging integrity is maintained during transportation; "
                "inspect seals and closures before dispatch."
            )
        if len(risks) < 2:
            risks.append(
                "Monitor storage conditions (temperature and humidity) regularly "
                "to prevent premature degradation."
            )

        return risks[:4]
