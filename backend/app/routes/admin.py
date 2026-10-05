"""
Admin routes — all endpoints require admin privileges.
"""
import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.food import FoodProfile
from ..models.packaging import PackagingMaterial
from ..models.recommendation import Recommendation
from ..models.user import User
from ..schemas.auth import UserResponse
from ..schemas.packaging import PackagingMaterialCreate, PackagingMaterialResponse
from ..schemas.recommendation import RecommendationListItem
from ..services.auth_service import AuthService
from ..utils.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


# ──────────────────────────────────────────────────────────────────────────────
# User management
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return all registered users."""
    return AuthService.get_all_users(db)


@router.put("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: str,
    is_active: bool,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Activate or deactivate a user account."""
    user = AuthService.update_user_status(db, user_id, is_active)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


# ──────────────────────────────────────────────────────────────────────────────
# System stats
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stats")
def system_stats(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return system-wide statistics."""
    total_users = db.query(User).count()
    total_recommendations = db.query(Recommendation).count()

    # Recommendations per day for last 7 days
    per_day: list[dict] = []
    now = datetime.utcnow()
    for i in range(6, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = (
            db.query(Recommendation)
            .filter(
                Recommendation.created_at >= day_start,
                Recommendation.created_at < day_end,
            )
            .count()
        )
        per_day.append({"date": day_start.strftime("%Y-%m-%d"), "count": count})

    return {
        "total_users": total_users,
        "total_recommendations": total_recommendations,
        "recommendations_per_day": per_day,
    }


# ──────────────────────────────────────────────────────────────────────────────
# All recommendations
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/recommendations", response_model=list[RecommendationListItem])
def list_all_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return all recommendations in the system (paginated)."""
    recs = (
        db.query(Recommendation)
        .order_by(Recommendation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_build_list_item(r, db) for r in recs]


# ──────────────────────────────────────────────────────────────────────────────
# Packaging materials (admin CRUD — duplicates public read + adds write)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/materials", response_model=list[PackagingMaterialResponse])
def list_materials(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return all packaging materials (admin view)."""
    materials = db.query(PackagingMaterial).order_by(PackagingMaterial.name).all()
    return [_serialize_material(m) for m in materials]


@router.post("/materials", response_model=PackagingMaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(
    material_data: PackagingMaterialCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Create a new packaging material."""
    import uuid

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
    return _serialize_material(material)


@router.put("/materials/{material_id}", response_model=PackagingMaterialResponse)
def update_material(
    material_id: str,
    material_data: PackagingMaterialCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Update a packaging material."""
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
    return _serialize_material(material)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_list_item(rec: Recommendation, db: Session) -> dict:
    food_name: Optional[str] = None
    fp = db.query(FoodProfile).filter(FoodProfile.id == rec.food_profile_id).first()
    if fp:
        food_name = fp.food_name  # FoodProfile.food_name  # FoodProfile.food_name

    primary_material_name: Optional[str] = None
    if rec.primary_material_id:
        mat = db.query(PackagingMaterial).filter(
            PackagingMaterial.id == rec.primary_material_id
        ).first()
        if mat:
            primary_material_name = mat.name

    return {
        "id": rec.id,
        "food_profile_id": rec.food_profile_id,
        "food_name": food_name,
        "primary_material_name": primary_material_name,
        "shelf_life_min_days": rec.shelf_life_min_days,
        "shelf_life_max_days": rec.shelf_life_max_days,
        "overall_score": rec.overall_score,
        "created_at": rec.created_at,
    }


def _serialize_material(material: PackagingMaterial) -> dict:
    d = {c.name: getattr(material, c.name) for c in material.__table__.columns}
    if hasattr(d.get("category"), "value"):
        d["category"] = d["category"].value
    if isinstance(d.get("suitable_for"), str):
        try:
            d["suitable_for"] = json.loads(d["suitable_for"])
        except (ValueError, TypeError):
            d["suitable_for"] = []
    return d
