"""
Packaging material routes.
"""
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.packaging import PackagingMaterial
from ..schemas.packaging import PackagingMaterialCreate, PackagingMaterialResponse
from ..utils.auth import get_current_admin

router = APIRouter(prefix="/packaging", tags=["Packaging Materials"])


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    """Return the distinct packaging material category values present in the DB."""
    rows = db.query(PackagingMaterial.category).distinct().all()
    return [str(r[0].value) if hasattr(r[0], "value") else str(r[0]) for r in rows]


@router.get("/", response_model=list[PackagingMaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    """Return all packaging materials (public endpoint)."""
    materials = db.query(PackagingMaterial).order_by(PackagingMaterial.name).all()
    return [_serialize(m) for m in materials]


@router.get("/{material_id}", response_model=PackagingMaterialResponse)
def get_material(material_id: str, db: Session = Depends(get_db)):
    """Return a single packaging material by ID."""
    material = db.query(PackagingMaterial).filter(PackagingMaterial.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found.")
    return _serialize(material)


@router.post("/", response_model=PackagingMaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(
    material_data: PackagingMaterialCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Create a new packaging material (admin only)."""
    existing = (
        db.query(PackagingMaterial)
        .filter(PackagingMaterial.material_code == material_data.material_code)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Material code '{material_data.material_code}' already exists.",
        )
    data = material_data.model_dump()
    if data.get("suitable_for") is not None:
        data["suitable_for"] = json.dumps(data["suitable_for"])
    material = PackagingMaterial(id=str(uuid.uuid4()), **data)
    db.add(material)
    db.commit()
    db.refresh(material)
    return _serialize(material)


@router.put("/{material_id}", response_model=PackagingMaterialResponse)
def update_material(
    material_id: str,
    material_data: PackagingMaterialCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Update a packaging material (admin only)."""
    material = db.query(PackagingMaterial).filter(PackagingMaterial.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found.")

    update_dict = material_data.model_dump()
    if update_dict.get("suitable_for") is not None:
        update_dict["suitable_for"] = json.dumps(update_dict["suitable_for"])

    for key, value in update_dict.items():
        setattr(material, key, value)

    db.commit()
    db.refresh(material)
    return _serialize(material)


# ──────────────────────────────────────────────────────────────────────────────
# Helper: deserialize JSON fields before returning to Pydantic
# ──────────────────────────────────────────────────────────────────────────────

def _serialize(material: PackagingMaterial) -> dict:
    """Convert ORM row to a dict with JSON fields decoded."""
    d = {c.name: getattr(material, c.name) for c in material.__table__.columns}
    # Decode suitable_for JSON string -> list
    if isinstance(d.get("suitable_for"), str):
        try:
            d["suitable_for"] = json.loads(d["suitable_for"])
        except (ValueError, TypeError):
            d["suitable_for"] = []
    # Decode category enum to string value
    if hasattr(d.get("category"), "value"):
        d["category"] = d["category"].value
    return d
