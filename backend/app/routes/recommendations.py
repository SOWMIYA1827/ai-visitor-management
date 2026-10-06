"""
Recommendation routes — POST to generate, GET to list/retrieve, PDF download.
"""
import json
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.food import FoodProfile
from ..models.packaging import PackagingMaterial
from ..models.recommendation import (
    PackagingRequirements,
    Recommendation,
    StorageConditions,
)
from ..models.user import User
from ..schemas.recommendation import (
    RecommendationListItem,
    RecommendationRequest,
    RecommendationResponse,
)
from ..ai.recommendation_engine import RecommendationEngine
from ..utils.auth import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# Module-level engine instance (loaded once)
_engine = RecommendationEngine()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get_or_create_food_profile(
    request: RecommendationRequest,
    db: Session,
    current_user: User,
) -> FoodProfile:
    """Return existing FoodProfile or create one from inline data."""
    if request.food_profile_id:
        fp = db.query(FoodProfile).filter(
            FoodProfile.id == request.food_profile_id,
            FoodProfile.user_id == current_user.id,
        ).first()
        if not fp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food profile not found.",
            )
        return fp

    if not request.food_profile:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either food_profile_id or food_profile must be provided.",
        )

    data = request.food_profile.model_dump()
    fp = FoodProfile(id=str(uuid.uuid4()), user_id=current_user.id, **data)
    db.add(fp)
    db.flush()  # get id without committing
    return fp


def _food_profile_to_dict(fp: FoodProfile) -> dict:
    return {
        "name": fp.food_name,
        "category": fp.category.value if fp.category else "other",
        "moisture_content": fp.moisture_content,
        "ph": fp.ph,
        "fat_content": fp.fat_content,
        "protein_content": fp.protein_content,
        "water_activity": fp.water_activity,
        "respiration_rate": fp.respiration_rate,
        "perishability": fp.perishability.value if fp.perishability else "medium",
        "oxygen_sensitivity": fp.oxygen_sensitivity.value if fp.oxygen_sensitivity else "low",
        "moisture_sensitivity": fp.moisture_sensitivity.value if fp.moisture_sensitivity else "low",
        "light_sensitivity": fp.light_sensitivity.value if fp.light_sensitivity else "low",
        "temperature_sensitivity": fp.temperature_sensitivity.value if fp.temperature_sensitivity else "low",
        "odor_sensitivity": fp.odor_sensitivity.value if fp.odor_sensitivity else "low",
        "microbial_sensitivity": fp.microbial_sensitivity.value if fp.microbial_sensitivity else "low",
    }


def _material_code_to_db_id(code: str, db: Session) -> Optional[str]:
    """Look up the DB id for a PackagingMaterial by material_code."""
    mat = db.query(PackagingMaterial).filter(PackagingMaterial.material_code == code).first()
    return mat.id if mat else None


def _build_response(rec: Recommendation, db: Session) -> dict:
    """Build a full response dict from an ORM Recommendation row."""
    # Fetch primary material
    primary_mat = None
    if rec.primary_material_id:
        primary_mat = db.query(PackagingMaterial).filter(
            PackagingMaterial.id == rec.primary_material_id
        ).first()

    # Fetch alternative materials
    alt_ids = json.loads(rec.alternative_material_ids) if rec.alternative_material_ids else []
    alt_mats = db.query(PackagingMaterial).filter(PackagingMaterial.id.in_(alt_ids)).all()

    # Food profile info
    food_name = None
    if rec.food_profile:
        food_name = rec.food_profile.food_name

    # Barrier properties
    barrier = json.loads(rec.barrier_properties) if rec.barrier_properties else {}
    risk_factors = json.loads(rec.risk_factors) if rec.risk_factors else []

    return {
        "id": rec.id,
        "user_id": rec.user_id,
        "food_profile_id": rec.food_profile_id,
        "food_name": food_name,
        "primary_material_id": rec.primary_material_id,
        "primary_material": primary_mat,
        "alternative_material_ids": alt_ids,
        "alternative_materials": alt_mats,
        "packaging_structure": rec.packaging_structure,
        "barrier_properties": barrier,
        "recommended_thickness_um": rec.recommended_thickness_um,
        "storage_conditions_recommended": rec.storage_conditions_recommended,
        "shelf_life_min_days": rec.shelf_life_min_days,
        "shelf_life_max_days": rec.shelf_life_max_days,
        "risk_factors": risk_factors,
        "sustainability_score": rec.sustainability_score,
        "cost_score": rec.cost_score,
        "food_safety_score": rec.food_safety_score,
        "overall_score": rec.overall_score,
        "explanation": rec.explanation,
        "created_at": rec.created_at,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI packaging recommendation.
    Accepts either an existing food_profile_id or inline food profile data.
    """
    # 1. Get or create food profile
    fp = _get_or_create_food_profile(request, db, current_user)
    food_dict = _food_profile_to_dict(fp)

    # 2. Build storage/packaging dicts
    storage_dict = request.storage_conditions.model_dump()
    pkg_dict = request.packaging_requirements.model_dump()
    # Convert enums to string values
    for key, val in storage_dict.items():
        if hasattr(val, "value"):
            storage_dict[key] = val.value
    for key, val in pkg_dict.items():
        if hasattr(val, "value"):
            pkg_dict[key] = val.value

    # 3. Run AI engine
    try:
        result = _engine.recommend(food_dict, storage_dict, pkg_dict)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation engine error: {str(exc)}",
        )

    # 4. Persist storage conditions
    sc = StorageConditions(
        id=str(uuid.uuid4()),
        **{k: v for k, v in storage_dict.items()
           if k in ["storage_temp", "storage_humidity", "storage_duration_days",
                    "transportation_duration_days", "cold_chain_required"]},
        transportation_type=request.storage_conditions.transportation_type,
    )
    db.add(sc)
    db.flush()

    # 5. Persist packaging requirements
    pr = PackagingRequirements(
        id=str(uuid.uuid4()),
        required_shelf_life_days=request.packaging_requirements.required_shelf_life_days,
        package_size=request.packaging_requirements.package_size,
        package_quantity=request.packaging_requirements.package_quantity,
        budget=request.packaging_requirements.budget,
        packaging_type=request.packaging_requirements.packaging_type,
        priority=request.packaging_requirements.priority,
        eco_preference=request.packaging_requirements.eco_preference,
    )
    db.add(pr)
    db.flush()

    # 6. Resolve material IDs from codes
    primary_mat_id = _material_code_to_db_id(result.primary_material_code, db)
    alt_ids = [
        mid for mid in (
            _material_code_to_db_id(code, db)
            for code in result.alternative_material_codes
        ) if mid
    ]

    # 7. Save recommendation
    rec = Recommendation(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        food_profile_id=fp.id,
        storage_conditions_id=sc.id,
        packaging_requirements_id=pr.id,
        primary_material_id=primary_mat_id,
        alternative_material_ids=json.dumps(alt_ids),
        packaging_structure=result.packaging_structure,
        barrier_properties=json.dumps(result.barrier_properties),
        recommended_thickness_um=result.recommended_thickness_um,
        storage_conditions_recommended=result.storage_conditions_recommended,
        shelf_life_min_days=result.shelf_life_min_days,
        shelf_life_max_days=result.shelf_life_max_days,
        risk_factors=json.dumps(result.risk_factors),
        sustainability_score=result.sustainability_score,
        cost_score=result.cost_score,
        food_safety_score=result.food_safety_score,
        overall_score=result.overall_score,
        explanation=result.explanation,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    return _build_response(rec, db)


@router.get("/", response_model=List[RecommendationListItem])
def list_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all recommendations for the authenticated user."""
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    result = []
    for rec in recs:
        food_name = rec.food_profile.food_name if rec.food_profile else None
        mat_name = rec.primary_material.name if rec.primary_material else None
        result.append(RecommendationListItem(
            id=rec.id,
            food_profile_id=rec.food_profile_id,
            food_name=food_name,
            primary_material_name=mat_name,
            shelf_life_min_days=rec.shelf_life_min_days,
            shelf_life_max_days=rec.shelf_life_max_days,
            overall_score=rec.overall_score,
            created_at=rec.created_at,
        ))
    return result


@router.get("/{recommendation_id}")
def get_recommendation(
    recommendation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single recommendation by ID."""
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id,
        )
        .first()
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")
    return _build_response(rec, db)


@router.get("/{recommendation_id}/risk")
def get_risk_analysis(
    recommendation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return structured risk analysis for a recommendation."""
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id,
        )
        .first()
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    risk_factors = json.loads(rec.risk_factors) if rec.risk_factors else []
    fp = rec.food_profile

    risks = []
    if fp:
        if fp.moisture_sensitivity and fp.moisture_sensitivity.value == "high":
            risks.append({"type": "Moisture Risk", "level": "High",
                          "mitigation": "Use high moisture-barrier film; include desiccant sachets."})
        elif fp.moisture_sensitivity and fp.moisture_sensitivity.value == "medium":
            risks.append({"type": "Moisture Risk", "level": "Medium",
                          "mitigation": "Maintain packaging integrity during storage."})

        if fp.oxygen_sensitivity and fp.oxygen_sensitivity.value == "high":
            risks.append({"type": "Oxidation Risk", "level": "High",
                          "mitigation": "Use oxygen barrier film or MAP; consider oxygen scavengers."})

        if fp.microbial_sensitivity and fp.microbial_sensitivity.value == "high":
            risks.append({"type": "Microbial Risk", "level": "High",
                          "mitigation": "Ensure hermetic seal; maintain cold chain; consider antimicrobial packaging."})

        if fp.light_sensitivity and fp.light_sensitivity.value == "high":
            risks.append({"type": "Light Exposure Risk", "level": "High",
                          "mitigation": "Use opaque or metallized packaging to block UV/visible light."})

        if fp.temperature_sensitivity and fp.temperature_sensitivity.value == "high":
            risks.append({"type": "Temperature Risk", "level": "High",
                          "mitigation": "Maintain cold chain; use insulated packaging for transport."})

    if not risks:
        risks.append({"type": "General Risk", "level": "Low",
                      "mitigation": "Follow standard GMP and storage guidelines."})

    return {
        "recommendation_id": recommendation_id,
        "risks": risks,
        "additional_factors": risk_factors,
        "disclaimer": (
            "PackSmart AI provides preliminary risk indications based on provided food properties. "
            "Laboratory testing and expert validation are required before commercial deployment."
        ),
    }


@router.get("/{recommendation_id}/sustainability")
def get_sustainability_analysis(
    recommendation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return sustainability analysis for a recommendation."""
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id,
        )
        .first()
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    primary_mat = rec.primary_material
    sustainability_data = {
        "recommendation_id": recommendation_id,
        "sustainability_score": rec.sustainability_score,
        "material_name": primary_mat.name if primary_mat else "N/A",
        "recyclable": primary_mat.recyclable if primary_mat else False,
        "biodegradable": primary_mat.biodegradable if primary_mat else False,
        "compostable": primary_mat.compostable if primary_mat else False,
        "bio_based": primary_mat.bio_based if primary_mat else False,
        "cost_index": primary_mat.cost_index if primary_mat else 0.5,
        "greener_alternatives": [],
        "trade_offs": (
            "Switching to biodegradable materials may increase cost and reduce shelf life. "
            "Evaluate trade-offs based on product requirements and market positioning."
        ),
        "disclaimer": "Environmental impact figures are indicative only and not validated by lifecycle analysis.",
    }

    # Find greener alternatives from alt materials
    alt_ids = json.loads(rec.alternative_material_ids) if rec.alternative_material_ids else []
    if alt_ids:
        alt_mats = db.query(PackagingMaterial).filter(PackagingMaterial.id.in_(alt_ids)).all()
        for mat in alt_mats:
            if mat.biodegradable or mat.recyclable or mat.compostable:
                sustainability_data["greener_alternatives"].append({
                    "name": mat.name,
                    "recyclable": mat.recyclable,
                    "biodegradable": mat.biodegradable,
                    "compostable": mat.compostable,
                })

    return sustainability_data


@router.get("/{recommendation_id}/report")
def download_report(
    recommendation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate and stream a PDF report for a recommendation."""
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id,
        )
        .first()
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    try:
        from ..utils.pdf_generator import generate_pdf_report
        pdf_bytes = generate_pdf_report(rec, db)
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="packsmart_report_{recommendation_id[:8]}.pdf"'
            },
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(exc)}",
        )


@router.post("/feedback")
def submit_feedback(
    recommendation_id: str,
    rating: int,
    comment: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit feedback for a recommendation (rating 1-5)."""
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=422, detail="Rating must be between 1 and 5.")

    rec = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == current_user.id,
    ).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    return {"message": "Feedback submitted successfully.", "rating": rating}
