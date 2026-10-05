"""
Seed the database with initial packaging materials knowledge base.
Safe to run multiple times (idempotent — skips existing records by material_code).
"""
import json

from sqlalchemy.orm import Session

from ..models.packaging import MaterialCategory, PackagingMaterial

# ---------------------------------------------------------------------------
# Packaging materials knowledge base
# ---------------------------------------------------------------------------
MATERIALS = [
    {
        "name": "Low-Density Polyethylene (LDPE)",
        "material_code": "LDPE",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.75,
        "oxygen_barrier": 0.30,
        "light_barrier": 0.20,
        "thermal_resistance": 0.35,
        "mechanical_strength": 0.40,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.25,
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 100.0,
        "description": (
            "Flexible, moisture-resistant film suitable for fresh produce, bread, and frozen foods. "
            "Low oxygen barrier; often used as inner liner in multilayer structures."
        ),
        "suitable_for": json.dumps(["vegetables", "fruits", "bakery", "cereals"]),
    },
    {
        "name": "High-Density Polyethylene (HDPE)",
        "material_code": "HDPE",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.85,
        "oxygen_barrier": 0.35,
        "light_barrier": 0.25,
        "thermal_resistance": 0.50,
        "mechanical_strength": 0.70,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.30,
        "typical_thickness_min_um": 25.0,
        "typical_thickness_max_um": 200.0,
        "description": (
            "Rigid or semi-rigid plastic with good moisture barrier. "
            "Used for milk jugs, juice bottles, grocery bags, and cereal box liners."
        ),
        "suitable_for": json.dumps(["dairy", "beverages", "cereals", "pulses"]),
    },
    {
        "name": "Polypropylene (PP)",
        "material_code": "PP",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.80,
        "oxygen_barrier": 0.40,
        "light_barrier": 0.20,
        "thermal_resistance": 0.65,
        "mechanical_strength": 0.65,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.30,
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 80.0,
        "description": (
            "Good moisture barrier with excellent heat resistance. "
            "Suitable for microwaveable trays, snack wrappers, and dairy containers."
        ),
        "suitable_for": json.dumps(["snacks", "dairy", "processed_food", "bakery"]),
    },
    {
        "name": "Biaxially Oriented Polypropylene (BOPP)",
        "material_code": "BOPP",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.82,
        "oxygen_barrier": 0.42,
        "light_barrier": 0.22,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.72,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.35,
        "typical_thickness_min_um": 15.0,
        "typical_thickness_max_um": 60.0,
        "description": (
            "Oriented PP film with superior clarity, stiffness, and moisture barrier. "
            "Widely used for snack food wrappers, biscuit packaging, and cereal bags."
        ),
        "suitable_for": json.dumps(["snacks", "cereals", "bakery", "pulses"]),
    },
    {
        "name": "Polyethylene Terephthalate (PET)",
        "material_code": "PET",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.78,
        "oxygen_barrier": 0.60,
        "light_barrier": 0.20,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.80,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.40,
        "typical_thickness_min_um": 12.0,
        "typical_thickness_max_um": 350.0,
        "description": (
            "High-clarity film/bottle resin with good gas barrier and mechanical strength. "
            "Used for beverage bottles, deli trays, and as outer layer in multilayer laminates."
        ),
        "suitable_for": json.dumps(["beverages", "processed_food", "dairy", "snacks"]),
    },
    {
        "name": "Metallized PET",
        "material_code": "MET-PET",
        "category": MaterialCategory.multilayer,
        "moisture_barrier": 0.92,
        "oxygen_barrier": 0.90,
        "light_barrier": 0.95,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.80,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.55,
        "typical_thickness_min_um": 12.0,
        "typical_thickness_max_um": 25.0,
        "description": (
            "PET film vacuum-coated with aluminium giving excellent barrier to oxygen, "
            "moisture and light. Used for crisps, nuts, spices, and long-shelf-life snacks."
        ),
        "suitable_for": json.dumps(["snacks", "spices", "cereals", "pulses"]),
    },
    {
        "name": "Aluminium Foil",
        "material_code": "ALU-FOIL",
        "category": MaterialCategory.metal,
        "moisture_barrier": 0.99,
        "oxygen_barrier": 0.99,
        "light_barrier": 1.00,
        "thermal_resistance": 0.85,
        "mechanical_strength": 0.50,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.65,
        "typical_thickness_min_um": 6.0,
        "typical_thickness_max_um": 150.0,
        "description": (
            "Complete barrier against moisture, oxygen, and light. "
            "Used in retort pouches, blister packs, chocolate wrappers, and aseptic cartons."
        ),
        "suitable_for": json.dumps(["dairy", "processed_food", "meat", "fish", "beverages"]),
    },
    {
        "name": "Paperboard",
        "material_code": "PAPERBOARD",
        "category": MaterialCategory.paper,
        "moisture_barrier": 0.30,
        "oxygen_barrier": 0.25,
        "light_barrier": 0.60,
        "thermal_resistance": 0.30,
        "mechanical_strength": 0.65,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "cost_index": 0.30,
        "typical_thickness_min_um": 200.0,
        "typical_thickness_max_um": 800.0,
        "description": (
            "Lightweight rigid board used for cereal boxes, frozen food cartons, beverage carriers. "
            "Typically coated or laminated for moisture resistance."
        ),
        "suitable_for": json.dumps(["cereals", "bakery", "beverages", "processed_food"]),
    },
    {
        "name": "Kraft Paper",
        "material_code": "KRAFT",
        "category": MaterialCategory.paper,
        "moisture_barrier": 0.20,
        "oxygen_barrier": 0.15,
        "light_barrier": 0.55,
        "thermal_resistance": 0.20,
        "mechanical_strength": 0.60,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "cost_index": 0.20,
        "typical_thickness_min_um": 40.0,
        "typical_thickness_max_um": 120.0,
        "description": (
            "Strong, natural brown paper used for flour bags, sugar sacks, and dry goods. "
            "Environmentally friendly; low barrier without coating."
        ),
        "suitable_for": json.dumps(["cereals", "pulses", "spices", "other"]),
    },
    {
        "name": "Glass Jar/Bottle",
        "material_code": "GLASS",
        "category": MaterialCategory.glass,
        "moisture_barrier": 1.00,
        "oxygen_barrier": 1.00,
        "light_barrier": 0.50,
        "thermal_resistance": 0.70,
        "mechanical_strength": 0.55,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.70,
        "typical_thickness_min_um": 1500.0,
        "typical_thickness_max_um": 5000.0,
        "description": (
            "Inert, impermeable container ideal for pickles, jams, sauces, and premium products. "
            "Heavy and fragile; amber glass provides light protection."
        ),
        "suitable_for": json.dumps(["dairy", "beverages", "processed_food", "spices"]),
    },
    {
        "name": "Polylactic Acid (PLA)",
        "material_code": "PLA",
        "category": MaterialCategory.biodegradable,
        "moisture_barrier": 0.55,
        "oxygen_barrier": 0.50,
        "light_barrier": 0.20,
        "thermal_resistance": 0.30,
        "mechanical_strength": 0.55,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": True,
        "compostable": True,
        "bio_based": True,
        "cost_index": 0.60,
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 60.0,
        "description": (
            "Bio-based and compostable film derived from corn/sugarcane starch. "
            "Suitable for fresh produce, bakery, and short shelf-life items where sustainability is priority."
        ),
        "suitable_for": json.dumps(["fruits", "vegetables", "bakery", "other"]),
    },
    {
        "name": "EVOH Barrier Film",
        "material_code": "EVOH",
        "category": MaterialCategory.multilayer,
        "moisture_barrier": 0.60,
        "oxygen_barrier": 0.97,
        "light_barrier": 0.30,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.70,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.70,
        "typical_thickness_min_um": 3.0,
        "typical_thickness_max_um": 15.0,
        "description": (
            "Exceptional oxygen barrier used as a core layer in multilayer films. "
            "Ideal for meat, cheese, and oxygen-sensitive processed foods."
        ),
        "suitable_for": json.dumps(["meat", "fish", "dairy", "processed_food"]),
    },
    {
        "name": "Nylon (Polyamide / PA)",
        "material_code": "PA",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.55,
        "oxygen_barrier": 0.70,
        "light_barrier": 0.20,
        "thermal_resistance": 0.75,
        "mechanical_strength": 0.85,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.55,
        "typical_thickness_min_um": 15.0,
        "typical_thickness_max_um": 50.0,
        "description": (
            "Strong film with good oxygen and puncture resistance. "
            "Used in vacuum pouches for meat, cheese, and high-barrier applications."
        ),
        "suitable_for": json.dumps(["meat", "fish", "dairy", "processed_food"]),
    },
    {
        "name": "Perforated LDPE Film",
        "material_code": "PERF-LDPE",
        "category": MaterialCategory.plastic,
        "moisture_barrier": 0.40,
        "oxygen_barrier": 0.10,
        "light_barrier": 0.10,
        "thermal_resistance": 0.35,
        "mechanical_strength": 0.35,
        "food_contact_safe": True,
        "recyclable": True,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.20,
        "typical_thickness_min_um": 20.0,
        "typical_thickness_max_um": 50.0,
        "description": (
            "LDPE film with micro-perforations allowing gas exchange, controlling respiration "
            "of fresh produce. Ideal for tomatoes, mushrooms, leafy vegetables."
        ),
        "suitable_for": json.dumps(["vegetables", "fruits"]),
    },
    {
        "name": "BOPP + PE Laminate",
        "material_code": "BOPP-PE",
        "category": MaterialCategory.multilayer,
        "moisture_barrier": 0.85,
        "oxygen_barrier": 0.45,
        "light_barrier": 0.25,
        "thermal_resistance": 0.55,
        "mechanical_strength": 0.75,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.40,
        "typical_thickness_min_um": 30.0,
        "typical_thickness_max_um": 80.0,
        "description": (
            "Two-layer laminate combining BOPP stiffness/clarity with PE heat-sealability "
            "and moisture barrier. Common for rice, flour, cereals, and pulses."
        ),
        "suitable_for": json.dumps(["cereals", "pulses", "spices", "snacks"]),
    },
    {
        "name": "Metallized PET + PE Laminate",
        "material_code": "MET-PET-PE",
        "category": MaterialCategory.multilayer,
        "moisture_barrier": 0.93,
        "oxygen_barrier": 0.91,
        "light_barrier": 0.96,
        "thermal_resistance": 0.60,
        "mechanical_strength": 0.82,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.58,
        "typical_thickness_min_um": 30.0,
        "typical_thickness_max_um": 70.0,
        "description": (
            "High-barrier laminate providing protection from moisture, oxygen, and light. "
            "Used for potato chips, nut mixes, and other premium snack products."
        ),
        "suitable_for": json.dumps(["snacks", "spices", "cereals", "pulses"]),
    },
    {
        "name": "Retort Pouch (Alu Foil Laminate)",
        "material_code": "RETORT-POUCH",
        "category": MaterialCategory.multilayer,
        "moisture_barrier": 0.99,
        "oxygen_barrier": 0.99,
        "light_barrier": 1.00,
        "thermal_resistance": 0.90,
        "mechanical_strength": 0.80,
        "food_contact_safe": True,
        "recyclable": False,
        "biodegradable": False,
        "compostable": False,
        "bio_based": False,
        "cost_index": 0.80,
        "typical_thickness_min_um": 80.0,
        "typical_thickness_max_um": 150.0,
        "description": (
            "PET/Alu/PP multilayer pouch withstanding retort sterilisation (121 °C). "
            "Used for ready-to-eat meals, curries, fish products, and shelf-stable foods."
        ),
        "suitable_for": json.dumps(["meat", "fish", "processed_food", "dairy"]),
    },
]


def run_seed(db: Session) -> None:
    """Insert missing packaging materials into the DB (idempotent)."""
    for mat_data in MATERIALS:
        existing = (
            db.query(PackagingMaterial)
            .filter(PackagingMaterial.material_code == mat_data["material_code"])
            .first()
        )
        if existing:
            continue
        material = PackagingMaterial(**mat_data)
        db.add(material)
    db.commit()
