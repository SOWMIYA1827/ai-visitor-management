from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..models.food import FoodCategory, PerishabilityLevel, SensitivityLevel


class FoodProfileCreate(BaseModel):
    food_name: str
    category: FoodCategory
    moisture_content: Optional[float] = None
    ph: Optional[float] = None
    fat_content: Optional[float] = None
    protein_content: Optional[float] = None
    water_activity: Optional[float] = None
    respiration_rate: Optional[float] = None
    perishability: Optional[PerishabilityLevel] = None
    oxygen_sensitivity: Optional[SensitivityLevel] = None
    moisture_sensitivity: Optional[SensitivityLevel] = None
    light_sensitivity: Optional[SensitivityLevel] = None
    temperature_sensitivity: Optional[SensitivityLevel] = None
    odor_sensitivity: Optional[SensitivityLevel] = None
    microbial_sensitivity: Optional[SensitivityLevel] = None


class FoodProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    food_name: str
    category: FoodCategory
    moisture_content: Optional[float] = None
    ph: Optional[float] = None
    fat_content: Optional[float] = None
    protein_content: Optional[float] = None
    water_activity: Optional[float] = None
    respiration_rate: Optional[float] = None
    perishability: Optional[PerishabilityLevel] = None
    oxygen_sensitivity: Optional[SensitivityLevel] = None
    moisture_sensitivity: Optional[SensitivityLevel] = None
    light_sensitivity: Optional[SensitivityLevel] = None
    temperature_sensitivity: Optional[SensitivityLevel] = None
    odor_sensitivity: Optional[SensitivityLevel] = None
    microbial_sensitivity: Optional[SensitivityLevel] = None
    created_at: datetime
