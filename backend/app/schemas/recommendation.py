from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from ..models.recommendation import EcoPreference, PackagingType, Priority, TransportationType
from .food import FoodProfileCreate
from .packaging import PackagingMaterialResponse


class StorageConditionsInput(BaseModel):
    storage_temp: Optional[float] = None
    storage_humidity: Optional[float] = None
    storage_duration_days: Optional[int] = None
    transportation_duration_days: Optional[int] = None
    transportation_type: Optional[TransportationType] = None
    cold_chain_required: bool = False


class PackagingRequirementsInput(BaseModel):
    required_shelf_life_days: Optional[int] = None
    package_size: Optional[str] = None
    package_quantity: Optional[int] = None
    budget: Optional[float] = None
    packaging_type: Optional[PackagingType] = None
    priority: Priority = Priority.balanced
    eco_preference: EcoPreference = EcoPreference.no_preference


class RecommendationRequest(BaseModel):
    """
    Accepts either an existing food_profile_id or inline food profile data.
    Both storage_conditions and packaging_requirements are required.
    """
    food_profile_id: Optional[str] = None
    food_profile: Optional[FoodProfileCreate] = None
    storage_conditions: StorageConditionsInput
    packaging_requirements: PackagingRequirementsInput


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    food_profile_id: str
    primary_material_id: Optional[str] = None
    alternative_material_ids: Optional[List[str]] = None
    primary_material: Optional[PackagingMaterialResponse] = None
    alternative_materials: Optional[List[PackagingMaterialResponse]] = None
    packaging_structure: Optional[str] = None
    barrier_properties: Optional[Dict[str, Any]] = None
    recommended_thickness_um: Optional[float] = None
    storage_conditions_recommended: Optional[str] = None
    shelf_life_min_days: Optional[int] = None
    shelf_life_max_days: Optional[int] = None
    risk_factors: Optional[List[str]] = None
    sustainability_score: Optional[float] = None
    cost_score: Optional[float] = None
    food_safety_score: Optional[float] = None
    overall_score: Optional[float] = None
    explanation: Optional[str] = None
    created_at: datetime


class RecommendationListItem(BaseModel):
    """Lightweight summary for dashboard listing."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    food_profile_id: str
    food_name: Optional[str] = None        # populated from joined food_profile
    primary_material_name: Optional[str] = None  # populated from joined material
    shelf_life_min_days: Optional[int] = None
    shelf_life_max_days: Optional[int] = None
    overall_score: Optional[float] = None
    created_at: datetime
