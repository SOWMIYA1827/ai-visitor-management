"""
Recommendation service — orchestrates AI engine calls and persists results.
"""
import json
import uuid
from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..ai.recommendation_engine import RecommendationEngine
from ..models.food import FoodProfile
from ..models.packaging import PackagingMaterial
from ..models.recommendation import PackagingRequirements, Recommendation, StorageConditions
from ..schemas.recommendation import PackagingRequirementsInput, RecommendationRequest, StorageConditionsInput

# Singleton engine — instantiated once, reused for all requests
_engine = RecommendationEngine()


class RecommendationService:
    """Stateless service; all methods receive a db Session."""

    @staticmethod
    def create_recommendation(
        db: Session,
        user_id: str,
        request: RecommendationRequest,
    ) -> Recommendation:
        """
        Full pipeline:
        1. Resolve or create the FoodProfile.
        2. Persist StorageConditions and PackagingRequirements rows.
        3. Call the AI engine.
        4. Resolve material IDs from material codes.
        5. Persist and return the Recommendation row.
        """
        # ── 1. Resolve food profile ──────────────────────────────────────────
        if request.food_profile_id:
            food_profile_row = (
                db.query(FoodProfile)
                .filter(
                    FoodProfile.id == request.food_profile_id,
                    FoodProfile.user_id == user_id,
                )
                .first()
            )
            if food_profile_row is None:
                raise ValueError(f"FoodProfile '{request.food_profile_id}' not found for this user.")
        elif request.food_profile:
            food_data = request.food_profile.model_dump()
            food_profile_row = FoodProfile(
                id=str(uuid.uuid4()),
                user_id=user_id,
                **food_data,
            )
            db.add(food_profile_row)
            db.flush()  # get the id without committing
        else:
            raise ValueError("Either food_profile_id or food_profile must be provided.")

        # ── 2. Persist storage conditions ────────────────────────────────────
        sc_data = request.storage_conditions.model_dump()
        storage_row = StorageConditions(
            id=str(uuid.uuid4()),
            **sc_data,
        )
        db.add(storage_row)
        db.flush()

        # ── 3. Persist packaging requirements ────────────────────────────────
        pr_data = request.packaging_requirements.model_dump()
        packaging_req_row = PackagingRequirements(
            id=str(uuid.uuid4()),
            **pr_data,
        )
        db.add(packaging_req_row)
        db.flush()

        # ── 4. Call AI engine ─────────────────────────────────────────────────
        # Engine expects plain dicts — use model_dump() on Pydantic objects
        food_dict = _orm_to_dict(food_profile_row)
        sc_dict = request.storage_conditions.model_dump()
        pr_dict = request.packaging_requirements.model_dump()

        result = _engine.recommend(food_dict, sc_dict, pr_dict)

        # ── 5. Resolve primary material ID ───────────────────────────────────
        primary_material = (
            db.query(PackagingMaterial)
            .filter(PackagingMaterial.material_code == result.primary_material_code)
            .first()
        )
        primary_material_id = primary_material.id if primary_material else None

        # ── 6. Resolve alternative material IDs ──────────────────────────────
        alt_ids: list[str] = []
        for code in result.alternative_material_codes:
            alt_mat = (
                db.query(PackagingMaterial)
                .filter(PackagingMaterial.material_code == code)
                .first()
            )
            if alt_mat:
                alt_ids.append(alt_mat.id)

        # ── 7. Build and persist Recommendation row ───────────────────────────
        rec = Recommendation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            food_profile_id=food_profile_row.id,
            storage_conditions_id=storage_row.id,
            packaging_requirements_id=packaging_req_row.id,
            primary_material_id=primary_material_id,
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
        return rec

    @staticmethod
    def get_user_recommendations(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Recommendation]:
        return (
            db.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .order_by(Recommendation.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_recommendation_by_id(
        db: Session,
        rec_id: str,
        user_id: str,
    ) -> Optional[Recommendation]:
        return (
            db.query(Recommendation)
            .filter(
                Recommendation.id == rec_id,
                Recommendation.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_stats(db: Session, user_id: str) -> dict[str, Any]:
        """
        Returns aggregated stats for a user's recommendations:
          total_count, avg_shelf_life (midpoint of min/max), avg_sustainability_score, avg_cost_score.
        """
        rows = (
            db.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .all()
        )
        if not rows:
            return {
                "total_count": 0,
                "avg_shelf_life": 0.0,
                "avg_sustainability_score": 0.0,
                "avg_cost_score": 0.0,
            }

        total = len(rows)
        avg_shelf = sum(
            ((r.shelf_life_min_days or 0) + (r.shelf_life_max_days or 0)) / 2.0
            for r in rows
        ) / total
        avg_sus = sum(r.sustainability_score or 0.0 for r in rows) / total
        avg_cost = sum(r.cost_score or 0.0 for r in rows) / total

        return {
            "total_count": total,
            "avg_shelf_life": round(avg_shelf, 1),
            "avg_sustainability_score": round(avg_sus, 2),
            "avg_cost_score": round(avg_cost, 2),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Helper: convert a SQLAlchemy ORM row to a plain dict for the AI engine
# ──────────────────────────────────────────────────────────────────────────────

def _orm_to_dict(obj: Any) -> dict[str, Any]:
    """Convert an ORM row to a plain dict, stringifying enum values."""
    result: dict[str, Any] = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        # Convert enum members to their string value
        if hasattr(val, "value"):
            val = val.value
        result[col.name] = val
    return result
