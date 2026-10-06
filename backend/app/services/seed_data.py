"""
Seed the database with packaging materials from knowledge_base.py and a default admin user.
Safe to run multiple times (idempotent — checks before inserting).
"""
import json
import uuid

from sqlalchemy.orm import Session

from ..ai.knowledge_base import PACKAGING_MATERIALS
from ..models.packaging import MaterialCategory, PackagingMaterial
from ..models.user import User, UserType
from ..utils.auth import get_password_hash

# ──────────────────────────────────────────────────────────────────────────────
# Category mapping from knowledge_base string -> MaterialCategory enum
# ──────────────────────────────────────────────────────────────────────────────
_CATEGORY_MAP: dict[str, MaterialCategory] = {
    "LDPE":            MaterialCategory.plastic,
    "HDPE":            MaterialCategory.plastic,
    "PP":              MaterialCategory.plastic,
    "BOPP":            MaterialCategory.plastic,
    "PET":             MaterialCategory.plastic,
    "MET-PET":         MaterialCategory.multilayer,
    "ALU-FOIL":        MaterialCategory.metal,
    "EVOH":            MaterialCategory.multilayer,
    "PAPERBOARD":      MaterialCategory.paper,
    "KRAFT":           MaterialCategory.paper,
    "GLASS":           MaterialCategory.glass,
    "PET-BOTTLE":      MaterialCategory.plastic,
    "HDPE-BOTTLE":     MaterialCategory.plastic,
    "PLA":             MaterialCategory.biodegradable,
    "BIO-FILM":        MaterialCategory.biodegradable,
    "PA":              MaterialCategory.plastic,
    "PERF-LDPE":       MaterialCategory.plastic,
    "BOPP-PE":         MaterialCategory.multilayer,
    "MET-PET-PE":      MaterialCategory.multilayer,
    "RETORT-POUCH":    MaterialCategory.multilayer,
    "VACUUM-PA-PE":    MaterialCategory.multilayer,
    "MAP-FILM":        MaterialCategory.multilayer,
    "MULTILAYER-PE-PA":MaterialCategory.multilayer,
    "PVC":             MaterialCategory.plastic,
}


def run_seed(db: Session) -> None:
    """
    Idempotent seed function.

    1. Insert all materials from knowledge_base.PACKAGING_MATERIALS into the DB
       (skips any whose material_code already exists).
    2. Create a default admin user if no admin exists yet.
    """
    _seed_materials(db)
    _seed_admin_user(db)


# ──────────────────────────────────────────────────────────────────────────────
# Materials
# ──────────────────────────────────────────────────────────────────────────────

def _seed_materials(db: Session) -> None:
    for code, mat in PACKAGING_MATERIALS.items():
        existing = (
            db.query(PackagingMaterial)
            .filter(PackagingMaterial.material_code == code)
            .first()
        )
        if existing:
            continue

        category = _CATEGORY_MAP.get(code, MaterialCategory.plastic)

        material = PackagingMaterial(
            id=str(uuid.uuid4()),
            name=mat["name"],
            material_code=mat["material_code"],
            category=category,
            moisture_barrier=mat.get("moisture_barrier", 0.5),
            oxygen_barrier=mat.get("oxygen_barrier", 0.5),
            light_barrier=mat.get("light_barrier", 0.5),
            thermal_resistance=mat.get("thermal_resistance", 0.5),
            mechanical_strength=mat.get("mechanical_strength", 0.5),
            food_contact_safe=mat.get("food_contact_safe", True),
            recyclable=mat.get("recyclable", False),
            biodegradable=mat.get("biodegradable", False),
            compostable=mat.get("compostable", False),
            bio_based=mat.get("bio_based", False),
            cost_index=mat.get("cost_index", 0.5),
            typical_thickness_min_um=mat.get("typical_thickness_min_um"),
            typical_thickness_max_um=mat.get("typical_thickness_max_um"),
            description=mat.get("description"),
            suitable_for=json.dumps(mat.get("suitable_categories", [])),
        )
        db.add(material)

    db.commit()


# ──────────────────────────────────────────────────────────────────────────────
# Admin user
# ──────────────────────────────────────────────────────────────────────────────

_DEFAULT_ADMIN_EMAIL = "admin@packsmart.ai"
_DEFAULT_ADMIN_PASSWORD = "Admin@123"


def _seed_admin_user(db: Session) -> None:
    # Check by email OR by is_admin flag — either means admin already seeded
    existing_admin = (
        db.query(User)
        .filter(
            (User.is_admin == True) | (User.email == _DEFAULT_ADMIN_EMAIL)  # noqa: E712
        )
        .first()
    )
    if existing_admin:
        return

    admin = User(
        id=str(uuid.uuid4()),
        email=_DEFAULT_ADMIN_EMAIL,
        hashed_password=get_password_hash(_DEFAULT_ADMIN_PASSWORD),
        full_name="PackSmart Admin",
        user_type=UserType.admin,
        organization="MoFPI / SIH 2026",
        is_active=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
