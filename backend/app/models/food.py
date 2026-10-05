import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from ..database import Base


class FoodCategory(str, enum.Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    cereals = "cereals"
    pulses = "pulses"
    spices = "spices"
    dairy = "dairy"
    meat = "meat"
    fish = "fish"
    bakery = "bakery"
    snacks = "snacks"
    processed_food = "processed_food"
    beverages = "beverages"
    other = "other"


class SensitivityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PerishabilityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class FoodProfile(Base):
    __tablename__ = "food_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    food_name = Column(String(255), nullable=False)
    category = Column(Enum(FoodCategory), nullable=False)

    # Composition properties
    moisture_content = Column(Float, nullable=True)   # percentage 0-100
    ph = Column(Float, nullable=True)                 # 0-14
    fat_content = Column(Float, nullable=True)        # percentage 0-100
    protein_content = Column(Float, nullable=True)    # percentage 0-100
    water_activity = Column(Float, nullable=True)     # aw 0-1
    respiration_rate = Column(Float, nullable=True)   # mg CO2/kg/h
    perishability = Column(Enum(PerishabilityLevel), nullable=True)

    # Sensitivity ratings
    oxygen_sensitivity = Column(Enum(SensitivityLevel), nullable=True)
    moisture_sensitivity = Column(Enum(SensitivityLevel), nullable=True)
    light_sensitivity = Column(Enum(SensitivityLevel), nullable=True)
    temperature_sensitivity = Column(Enum(SensitivityLevel), nullable=True)
    odor_sensitivity = Column(Enum(SensitivityLevel), nullable=True)
    microbial_sensitivity = Column(Enum(SensitivityLevel), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="food_profiles")
    recommendations = relationship("Recommendation", back_populates="food_profile", cascade="all, delete-orphan")
