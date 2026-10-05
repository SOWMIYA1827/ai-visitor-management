from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from ..models.packaging import MaterialCategory


class PackagingMaterialCreate(BaseModel):
    name: str
    material_code: str
    category: MaterialCategory
    moisture_barrier: float = 0.5
    oxygen_barrier: float = 0.5
    light_barrier: float = 0.5
    thermal_resistance: float = 0.5
    mechanical_strength: float = 0.5
    food_contact_safe: bool = True
    recyclable: bool = False
    biodegradable: bool = False
    compostable: bool = False
    bio_based: bool = False
    cost_index: float = 0.5
    typical_thickness_min_um: Optional[float] = None
    typical_thickness_max_um: Optional[float] = None
    description: Optional[str] = None
    suitable_for: Optional[List[str]] = None  # list of FoodCategory strings


class PackagingMaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    material_code: str
    category: MaterialCategory
    moisture_barrier: float
    oxygen_barrier: float
    light_barrier: float
    thermal_resistance: float
    mechanical_strength: float
    food_contact_safe: bool
    recyclable: bool
    biodegradable: bool
    compostable: bool
    bio_based: bool
    cost_index: float
    typical_thickness_min_um: Optional[float] = None
    typical_thickness_max_um: Optional[float] = None
    description: Optional[str] = None
    suitable_for: Optional[List[str]] = None
    created_at: datetime
