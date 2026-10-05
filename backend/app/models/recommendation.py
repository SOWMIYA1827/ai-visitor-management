import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class TransportationType(str, enum.Enum):
    road = "road"
    rail = "rail"
    air = "air"
    sea = "sea"


class PackagingType(str, enum.Enum):
    pouch = "pouch"
    bag = "bag"
    bottle = "bottle"
    tray = "tray"
    box = "box"
    vacuum_pack = "vacuum_pack"
    map = "map"          # Modified Atmosphere Packaging
    flexible = "flexible"
    rigid = "rigid"


class Priority(str, enum.Enum):
    low_cost = "low_cost"
    max_shelf_life = "max_shelf_life"
    food_safety = "food_safety"
    sustainability = "sustainability"
    balanced = "balanced"


class EcoPreference(str, enum.Enum):
    no_preference = "no_preference"
    recyclable = "recyclable"
    biodegradable = "biodegradable"
    compostable = "compostable"
    bio_based = "bio_based"


class StorageConditions(Base):
    __tablename__ = "storage_conditions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    storage_temp = Column(Float, nullable=True)               # °C
    storage_humidity = Column(Float, nullable=True)           # % RH
    storage_duration_days = Column(Integer, nullable=True)
    transportation_duration_days = Column(Integer, nullable=True)
    transportation_type = Column(Enum(TransportationType), nullable=True)
    cold_chain_required = Column(Boolean, default=False, nullable=False)

    # Back-reference
    recommendation = relationship("Recommendation", back_populates="storage_conditions_obj", uselist=False)


class PackagingRequirements(Base):
    __tablename__ = "packaging_requirements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    required_shelf_life_days = Column(Integer, nullable=True)
    package_size = Column(String(100), nullable=True)
    package_quantity = Column(Integer, nullable=True)
    budget = Column(Float, nullable=True)                     # INR or generic currency unit
    packaging_type = Column(Enum(PackagingType), nullable=True)
    priority = Column(Enum(Priority), nullable=True, default=Priority.balanced)
    eco_preference = Column(Enum(EcoPreference), nullable=True, default=EcoPreference.no_preference)

    # Back-reference
    recommendation = relationship("Recommendation", back_populates="packaging_requirements_obj", uselist=False)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    food_profile_id = Column(String(36), ForeignKey("food_profiles.id"), nullable=False, index=True)

    # FK to child tables (1-to-1)
    storage_conditions_id = Column(String(36), ForeignKey("storage_conditions.id"), nullable=True)
    packaging_requirements_id = Column(String(36), ForeignKey("packaging_requirements.id"), nullable=True)

    # Primary material FK
    primary_material_id = Column(String(36), ForeignKey("packaging_materials.id"), nullable=True)

    # Alternative materials stored as JSON array of material IDs
    alternative_material_ids = Column(Text, nullable=True)  # JSON

    # Recommendation output
    packaging_structure = Column(Text, nullable=True)
    barrier_properties = Column(Text, nullable=True)         # JSON object
    recommended_thickness_um = Column(Float, nullable=True)
    storage_conditions_recommended = Column(Text, nullable=True)
    shelf_life_min_days = Column(Integer, nullable=True)
    shelf_life_max_days = Column(Integer, nullable=True)
    risk_factors = Column(Text, nullable=True)               # JSON array
    sustainability_score = Column(Float, nullable=True)      # 0-100
    cost_score = Column(Float, nullable=True)                # 0-100
    food_safety_score = Column(Float, nullable=True)         # 0-100
    overall_score = Column(Float, nullable=True)             # 0-100
    explanation = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    food_profile = relationship("FoodProfile", back_populates="recommendations")
    primary_material = relationship(
        "PackagingMaterial",
        back_populates="primary_recommendations",
        foreign_keys=[primary_material_id],
    )
    storage_conditions_obj = relationship("StorageConditions", back_populates="recommendation")
    packaging_requirements_obj = relationship("PackagingRequirements", back_populates="recommendation")
