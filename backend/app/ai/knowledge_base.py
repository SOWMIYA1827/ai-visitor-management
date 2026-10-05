"""
Packaging materials knowledge base.

Each entry is keyed by material_code and contains all barrier scores,
sustainability flags, food compatibility rules, and physical specifications.
This is the authoritative static dataset used by the rule engine and scoring engine.
"""
from typing import Any

# ──────────────────────────────────────────────────────────────────────────────
# Type hint alias for a material entry dict
# ──────────────────────────────────────────────────────────────────────────────
# material_code       : str   — unique identifier (matches DB material_code)
# name                : str   — human-readable name
# moisture_barrier    : float — 0-1 scale (1 = perfect barrier)
# oxygen_barrier      : float — 0-1 scale
# light_barrier       : float — 0-1 scale
# thermal_resistance  : float — 0-1 scale
# mechanical_strength : float — 0-1 scale
# cost_index          : float — 0-1 (0=cheapest, 1=most expensive)
# recyclable          : bool
# biodegradable       : bool
# compostable         : bool
# bio_based           : bool
# food_contact_safe   : bool  — must be True for any recommendation
# suitable_categories : list[str]  — food category strings from FoodCategory enum
# unsuitable_for      : list[str]  — restriction tags, e.g. "high_fat", "acidic"
# description         : str
# typical_thickness_min_um : float — micrometres
# typical_thickness_max_um : float — micrometres
# shelf_life_multiplier    : float — relative multiplier applied to perishability baseline


PACKAGING_MATERIALS: dict[str, dict[str, Any]] = {

    # ── Polyolefins ────────────────────────────────────────────────────────────

    "LDPE": {
        "material_code": "LDPE",
        "name": "Low-Density Polyethylene (LDPE)",
        "moisture_barrier": 0.75,
        "oxygen_barrier": 0.30,
        "light_barrier": 0.20,
        "thermal_resistance": 0.35,
        "mechanical_strength": 0.40,
        "cost_index": 0.25,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": [
            "vegetables", "fruits", "bakery", "cereals",
        ],
        "unsuitable_for": [],
        "description": (
            "Flexible, moisture-resistant film suitable for fresh produce, bread, and frozen foods. "
            "Low oxygen barrier; often used as inner liner in multilayer structures."
        ),
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 100.0,
        "shelf_life_multiplier": 1.1,
    },

    "HDPE": {
        "material_code": "HDPE",
        "name": "High-Density Polyethylene (HDPE)",
        "moisture_barrier": 0.85,
        "oxygen_barrier": 0.35,
        "light_barrier": 0.25,
        "thermal_resistance": 0.50,
        "mechanical_strength": 0.70,
        "cost_index": 0.30,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["dairy", "beverages", "cereals", "pulses"],
        "unsuitable_for": [],
        "description": (
            "Rigid or semi-rigid plastic with good moisture barrier. "
            "Used for milk jugs, juice bottles, grocery bags, and cereal box liners."
        ),
        "typical_thickness_min_um": 25.0,
        "typical_thickness_max_um": 200.0,
        "shelf_life_multiplier": 1.2,
    },

    "PP": {
        "material_code": "PP",
        "name": "Polypropylene (PP)",
        "moisture_barrier": 0.80,
        "oxygen_barrier": 0.40,
        "light_barrier": 0.20,
        "thermal_resistance": 0.65,
        "mechanical_strength": 0.65,
        "cost_index": 0.30,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["snacks", "dairy", "processed_food", "bakery"],
        "unsuitable_for": [],
        "description": (
            "Good moisture barrier with excellent heat resistance. "
            "Suitable for microwaveable trays, snack wrappers, and dairy containers."
        ),
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 80.0,
        "shelf_life_multiplier": 1.15,
    },

    "BOPP": {
        "material_code": "BOPP",
        "name": "Biaxially Oriented Polypropylene (BOPP)",
        "moisture_barrier": 0.82,
        "oxygen_barrier": 0.42,
        "light_barrier": 0.22,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.72,
        "cost_index": 0.35,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["snacks", "cereals", "bakery", "pulses"],
        "unsuitable_for": [],
        "description": (
            "Oriented PP film with superior clarity, stiffness, and moisture barrier. "
            "Widely used for snack food wrappers, biscuit packaging, and cereal bags."
        ),
        "typical_thickness_min_um": 15.0,
        "typical_thickness_max_um": 60.0,
        "shelf_life_multiplier": 1.2,
    },

    "PET": {
        "material_code": "PET",
        "name": "Polyethylene Terephthalate (PET)",
        "moisture_barrier": 0.78,
        "oxygen_barrier": 0.60,
        "light_barrier": 0.20,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.80,
        "cost_index": 0.40,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["beverages", "processed_food", "dairy", "snacks"],
        "unsuitable_for": [],
        "description": (
            "High-clarity film/bottle resin with good gas barrier and mechanical strength. "
            "Used for beverage bottles, deli trays, and as outer layer in multilayer laminates."
        ),
        "typical_thickness_min_um": 12.0,
        "typical_thickness_max_um": 350.0,
        "shelf_life_multiplier": 1.3,
    },

    # ── High-barrier films ─────────────────────────────────────────────────────

    "MET-PET": {
        "material_code": "MET-PET",
        "name": "Metallized PET",
        "moisture_barrier": 0.92,
        "oxygen_barrier": 0.90,
        "light_barrier": 0.95,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.80,
        "cost_index": 0.55,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["snacks", "spices", "cereals", "pulses"],
        "unsuitable_for": [],
        "description": (
            "PET film vacuum-coated with aluminium giving excellent barrier to oxygen, "
            "moisture, and light. Used for crisps, nuts, spices, and long-shelf-life snacks."
        ),
        "typical_thickness_min_um": 12.0,
        "typical_thickness_max_um": 25.0,
        "shelf_life_multiplier": 1.8,
    },

    "ALU-FOIL": {
        "material_code": "ALU-FOIL",
        "name": "Aluminium Foil",
        "moisture_barrier": 0.99,
        "oxygen_barrier": 0.99,
        "light_barrier": 1.00,
        "thermal_resistance": 0.85,
        "mechanical_strength": 0.50,
        "cost_index": 0.65,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["dairy", "processed_food", "meat", "fish", "beverages"],
        "unsuitable_for": ["acidic"],  # bare foil + acidic food = corrosion risk
        "description": (
            "Complete barrier against moisture, oxygen, and light. "
            "Used in retort pouches, blister packs, chocolate wrappers, and aseptic cartons."
        ),
        "typical_thickness_min_um": 6.0,
        "typical_thickness_max_um": 150.0,
        "shelf_life_multiplier": 2.0,
    },

    "EVOH": {
        "material_code": "EVOH",
        "name": "EVOH Barrier Film",
        "moisture_barrier": 0.60,
        "oxygen_barrier": 0.97,
        "light_barrier": 0.30,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.70,
        "cost_index": 0.70,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["meat", "fish", "dairy", "processed_food"],
        "unsuitable_for": ["high_humidity_storage"],
        "description": (
            "Exceptional oxygen barrier used as a core layer in multilayer films. "
            "Ideal for meat, cheese, and oxygen-sensitive processed foods."
        ),
        "typical_thickness_min_um": 3.0,
        "typical_thickness_max_um": 15.0,
        "shelf_life_multiplier": 2.5,
    },

    # ── Paper / board ──────────────────────────────────────────────────────────

    "PAPERBOARD": {
        "material_code": "PAPERBOARD",
        "name": "Paperboard",
        "moisture_barrier": 0.30,
        "oxygen_barrier": 0.25,
        "light_barrier": 0.60,
        "thermal_resistance": 0.30,
        "mechanical_strength": 0.65,
        "cost_index": 0.30,
        "recyclable": True,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "food_contact_safe": True,
        "suitable_categories": ["cereals", "bakery", "beverages", "processed_food"],
        "unsuitable_for": ["high_moisture", "high_fat"],
        "description": (
            "Lightweight rigid board used for cereal boxes, frozen food cartons, beverage carriers. "
            "Typically coated or laminated for moisture resistance."
        ),
        "typical_thickness_min_um": 200.0,
        "typical_thickness_max_um": 800.0,
        "shelf_life_multiplier": 1.0,
    },

    "KRAFT": {
        "material_code": "KRAFT",
        "name": "Kraft Paper",
        "moisture_barrier": 0.20,
        "oxygen_barrier": 0.15,
        "light_barrier": 0.55,
        "thermal_resistance": 0.20,
        "mechanical_strength": 0.60,
        "cost_index": 0.20,
        "recyclable": True,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "food_contact_safe": True,
        "suitable_categories": ["cereals", "pulses", "spices", "other"],
        "unsuitable_for": ["high_moisture", "high_fat", "beverages"],
        "description": (
            "Strong, natural brown paper used for flour bags, sugar sacks, and dry goods. "
            "Environmentally friendly; low barrier without coating."
        ),
        "typical_thickness_min_um": 40.0,
        "typical_thickness_max_um": 120.0,
        "shelf_life_multiplier": 0.9,
    },

    # ── Glass ──────────────────────────────────────────────────────────────────

    "GLASS": {
        "material_code": "GLASS",
        "name": "Glass Jar/Bottle",
        "moisture_barrier": 1.00,
        "oxygen_barrier": 1.00,
        "light_barrier": 0.50,
        "thermal_resistance": 0.70,
        "mechanical_strength": 0.55,
        "cost_index": 0.70,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["dairy", "beverages", "processed_food", "spices"],
        "unsuitable_for": [],
        "description": (
            "Inert, impermeable container ideal for pickles, jams, sauces, and premium products. "
            "Heavy and fragile; amber glass provides additional light protection."
        ),
        "typical_thickness_min_um": 1500.0,
        "typical_thickness_max_um": 5000.0,
        "shelf_life_multiplier": 2.0,
    },

    "PET-BOTTLE": {
        "material_code": "PET-BOTTLE",
        "name": "PET Bottle",
        "moisture_barrier": 0.80,
        "oxygen_barrier": 0.62,
        "light_barrier": 0.20,
        "thermal_resistance": 0.58,
        "mechanical_strength": 0.78,
        "cost_index": 0.42,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["beverages", "dairy", "processed_food"],
        "unsuitable_for": [],
        "description": (
            "Blow-moulded PET bottle with good clarity and moderate gas barrier. "
            "Standard for carbonated and non-carbonated beverages, cooking oils, and sauces."
        ),
        "typical_thickness_min_um": 200.0,
        "typical_thickness_max_um": 500.0,
        "shelf_life_multiplier": 1.4,
    },

    "HDPE-BOTTLE": {
        "material_code": "HDPE-BOTTLE",
        "name": "HDPE Bottle",
        "moisture_barrier": 0.87,
        "oxygen_barrier": 0.38,
        "light_barrier": 0.30,
        "thermal_resistance": 0.52,
        "mechanical_strength": 0.72,
        "cost_index": 0.33,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["dairy", "beverages", "processed_food"],
        "unsuitable_for": [],
        "description": (
            "Rigid HDPE bottle with excellent moisture barrier. "
            "Used for milk, juice, water, shampoos, and household liquids."
        ),
        "typical_thickness_min_um": 300.0,
        "typical_thickness_max_um": 600.0,
        "shelf_life_multiplier": 1.3,
    },

    # ── Biodegradable / bio-based ──────────────────────────────────────────────

    "PLA": {
        "material_code": "PLA",
        "name": "Polylactic Acid (PLA)",
        "moisture_barrier": 0.55,
        "oxygen_barrier": 0.50,
        "light_barrier": 0.20,
        "thermal_resistance": 0.30,
        "mechanical_strength": 0.55,
        "cost_index": 0.60,
        "recyclable": False,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "food_contact_safe": True,
        "suitable_categories": ["fruits", "vegetables", "bakery", "other"],
        "unsuitable_for": ["high_temperature_storage"],
        "description": (
            "Bio-based and compostable film derived from corn/sugarcane starch. "
            "Suitable for fresh produce, bakery, and short shelf-life items where sustainability is priority."
        ),
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 60.0,
        "shelf_life_multiplier": 1.0,
    },

    "BIO-FILM": {
        "material_code": "BIO-FILM",
        "name": "Biodegradable Film",
        "moisture_barrier": 0.50,
        "oxygen_barrier": 0.45,
        "light_barrier": 0.20,
        "thermal_resistance": 0.25,
        "mechanical_strength": 0.45,
        "cost_index": 0.65,
        "recyclable": False,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "food_contact_safe": True,
        "suitable_categories": ["fruits", "vegetables", "bakery", "other"],
        "unsuitable_for": ["high_temperature_storage", "high_fat"],
        "description": (
            "PBAT/starch blend film that degrades in composting conditions. "
            "Suitable for fresh produce overwrapping and short-shelf-life bakery items."
        ),
        "typical_thickness_min_um": 15.0,
        "typical_thickness_max_um": 50.0,
        "shelf_life_multiplier": 0.95,
    },

    # ── Multilayer / specialty ─────────────────────────────────────────────────

    "PA": {
        "material_code": "PA",
        "name": "Nylon (Polyamide / PA)",
        "moisture_barrier": 0.55,
        "oxygen_barrier": 0.70,
        "light_barrier": 0.20,
        "thermal_resistance": 0.75,
        "mechanical_strength": 0.85,
        "cost_index": 0.55,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["meat", "fish", "dairy", "processed_food"],
        "unsuitable_for": [],
        "description": (
            "Strong film with good oxygen and puncture resistance. "
            "Used in vacuum pouches for meat, cheese, and high-barrier applications."
        ),
        "typical_thickness_min_um": 15.0,
        "typical_thickness_max_um": 50.0,
        "shelf_life_multiplier": 1.5,
    },

    "PERF-LDPE": {
        "material_code": "PERF-LDPE",
        "name": "Perforated LDPE Film",
        "moisture_barrier": 0.40,
        "oxygen_barrier": 0.10,
        "light_barrier": 0.10,
        "thermal_resistance": 0.35,
        "mechanical_strength": 0.35,
        "cost_index": 0.20,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["vegetables", "fruits"],
        "unsuitable_for": [
            "high_oxygen_sensitivity", "high_moisture_sensitivity",
        ],
        "description": (
            "LDPE film with micro-perforations allowing gas exchange, controlling respiration "
            "of fresh produce. Ideal for tomatoes, mushrooms, and leafy vegetables."
        ),
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 50.0,
        "shelf_life_multiplier": 1.05,
    },

    "BOPP-PE": {
        "material_code": "BOPP-PE",
        "name": "BOPP + PE Laminate",
        "moisture_barrier": 0.85,
        "oxygen_barrier": 0.45,
        "light_barrier": 0.25,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.75,
        "cost_index": 0.40,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["cereals", "pulses", "spices", "snacks"],
        "unsuitable_for": [],
        "description": (
            "Two-layer laminate combining BOPP stiffness/clarity with PE heat-sealability "
            "and moisture barrier. Common for rice, flour, cereals, and pulses."
        ),
        "typical_thickness_min_um": 30.0,
        "typical_thickness_max_um": 80.0,
        "shelf_life_multiplier": 1.35,
    },

    "MET-PET-PE": {
        "material_code": "MET-PET-PE",
        "name": "Metallized PET + PE Laminate",
        "moisture_barrier": 0.93,
        "oxygen_barrier": 0.91,
        "light_barrier": 0.96,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.82,
        "cost_index": 0.58,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["snacks", "spices", "cereals", "pulses"],
        "unsuitable_for": [],
        "description": (
            "High-barrier laminate providing protection from moisture, oxygen, and light. "
            "Used for potato chips, nut mixes, and other premium snack products."
        ),
        "typical_thickness_min_um": 30.0,
        "typical_thickness_max_um": 70.0,
        "shelf_life_multiplier": 2.0,
    },

    "RETORT-POUCH": {
        "material_code": "RETORT-POUCH",
        "name": "Retort Pouch (Alu Foil Laminate)",
        "moisture_barrier": 0.99,
        "oxygen_barrier": 0.99,
        "light_barrier": 1.00,
        "thermal_resistance": 0.90,
        "mechanical_strength": 0.80,
        "cost_index": 0.80,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["meat", "fish", "processed_food", "dairy"],
        "unsuitable_for": [],
        "description": (
            "PET/Alu/PP multilayer pouch withstanding retort sterilisation (121°C). "
            "Used for ready-to-eat meals, curries, fish products, and shelf-stable foods."
        ),
        "typical_thickness_min_um": 80.0,
        "typical_thickness_max_um": 150.0,
        "shelf_life_multiplier": 3.0,
    },

    "VACUUM-PA-PE": {
        "material_code": "VACUUM-PA-PE",
        "name": "Vacuum Pouch (PA/PE)",
        "moisture_barrier": 0.88,
        "oxygen_barrier": 0.80,
        "light_barrier": 0.22,
        "thermal_resistance": 0.70,
        "mechanical_strength": 0.88,
        "cost_index": 0.55,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": ["meat", "fish", "dairy", "processed_food"],
        "unsuitable_for": [],
        "description": (
            "Nylon/PE coextruded film used in vacuum packing of meat, cheese, and cured products. "
            "High puncture resistance and good oxygen barrier extend shelf life significantly."
        ),
        "typical_thickness_min_um": 60.0,
        "typical_thickness_max_um": 120.0,
        "shelf_life_multiplier": 2.2,
    },

    "MAP-FILM": {
        "material_code": "MAP-FILM",
        "name": "MAP Film (Modified Atmosphere)",
        "moisture_barrier": 0.75,
        "oxygen_barrier": 0.72,
        "light_barrier": 0.25,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.70,
        "cost_index": 0.60,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": [
            "meat", "fish", "dairy", "fruits", "vegetables", "bakery",
        ],
        "unsuitable_for": [],
        "description": (
            "Selectively permeable multilayer film designed for Modified Atmosphere Packaging. "
            "Controls CO2/O2 ratios to suppress microbial growth and slow respiration."
        ),
        "typical_thickness_min_um": 40.0,
        "typical_thickness_max_um": 100.0,
        "shelf_life_multiplier": 2.0,
    },

    "MULTILAYER-PE-PA": {
        "material_code": "MULTILAYER-PE-PA",
        "name": "Multilayer PE/PA Film",
        "moisture_barrier": 0.86,
        "oxygen_barrier": 0.78,
        "light_barrier": 0.22,
        "thermal_resistance": 0.68,
        "mechanical_strength": 0.84,
        "cost_index": 0.52,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,
        "suitable_categories": [
            "meat", "fish", "dairy", "processed_food", "snacks",
        ],
        "unsuitable_for": [],
        "description": (
            "Coextruded PE/PA/PE film combining toughness (PA) with moisture resistance (PE). "
            "Versatile barrier film used in form-fill-seal and vacuum applications."
        ),
        "typical_thickness_min_um": 50.0,
        "typical_thickness_max_um": 150.0,
        "shelf_life_multiplier": 1.9,
    },

    # ── PVC (restricted use) ───────────────────────────────────────────────────

    "PVC": {
        "material_code": "PVC",
        "name": "PVC Stretch Film",
        "moisture_barrier": 0.65,
        "oxygen_barrier": 0.50,
        "light_barrier": 0.15,
        "thermal_resistance": 0.45,
        "mechanical_strength": 0.60,
        "cost_index": 0.30,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "food_contact_safe": True,  # food-grade PVC is approved; avoided when possible
        "suitable_categories": ["meat", "vegetables", "fruits"],
        "unsuitable_for": ["high_temperature_storage", "microwave"],
        "description": (
            "Cling film widely used for retail fresh-meat and produce overwrap. "
            "Regulatory restrictions exist in some markets; prefer LDPE/PE alternatives."
        ),
        "typical_thickness_min_um": 8.0,
        "typical_thickness_max_um": 25.0,
        "shelf_life_multiplier": 1.0,
    },
}

# ── Quick-lookup helpers ───────────────────────────────────────────────────────

MATERIAL_CODES: list[str] = list(PACKAGING_MATERIALS.keys())


def get_material(code: str) -> dict[str, Any]:
    """Return the material dict for *code*, raising KeyError if not found."""
    return PACKAGING_MATERIALS[code]
