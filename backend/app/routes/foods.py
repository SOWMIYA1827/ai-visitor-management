"""
Food profile routes.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.food import FoodProfile
from ..models.user import User
from ..schemas.food import FoodProfileCreate, FoodProfileResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/foods", tags=["Food Profiles"])


@router.post("/", response_model=FoodProfileResponse, status_code=status.HTTP_201_CREATED)
def create_food_profile(
    food_data: FoodProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new food profile for the authenticated user."""
    profile = FoodProfile(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        **food_data.model_dump(),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/", response_model=list[FoodProfileResponse])
def list_food_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all food profiles belonging to the authenticated user."""
    return (
        db.query(FoodProfile)
        .filter(FoodProfile.user_id == current_user.id)
        .order_by(FoodProfile.created_at.desc())
        .all()
    )


@router.get("/{food_id}", response_model=FoodProfileResponse)
def get_food_profile(
    food_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single food profile; validates ownership."""
    profile = (
        db.query(FoodProfile)
        .filter(FoodProfile.id == food_id, FoodProfile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food profile not found.")
    return profile


@router.delete("/{food_id}")
def delete_food_profile(
    food_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a food profile; validates ownership."""
    profile = (
        db.query(FoodProfile)
        .filter(FoodProfile.id == food_id, FoodProfile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food profile not found.")
    db.delete(profile)
    db.commit()
    return {"message": "Food profile deleted successfully."}
