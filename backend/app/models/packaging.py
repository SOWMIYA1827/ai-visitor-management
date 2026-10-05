import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class MaterialCategory(str, enum.Enum):
    plastic = "plastic"
    paper = "paper"
    metal = "metal"
    glass = "glass"
    biodegradable = "biodegradable"
    multilayer = "multilayer"
    composite = "composite"


class PackagingMaterial(Base):
    __tablename__ = "packaging_materials"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(255), nullable=False, unique=True)
    material_code = Column(String(50), nullable=False, unique=True, index=True)
    category = Column(Enum(MaterialCategory), nullable=False)

    # Barrier properties (0.0 – 1.0 scale; higher = better barrier)
    moisture_barrier = Column(Float, nullable=False, default=0.5)
    oxygen_barrier = Column(Float, nullable=False, default=0.5)
    light_barrier = Column(Float, nullable=False, default=0.5)
    thermal_resistance = Column(Float, nullable=False, default=0.5)
    mechanical_strength = Column(Float, nullable=False, default=0.5)

    # Compliance & sustainability flags
    food_contact_safe = Column(Boolean, nullable=False, default=True)
    recyclable = Column(Boolean, nullable=False, default=False)
    biodegradable = Column(Boolean, nullable=False, default=False)
    compostable = Column(Boolean, nullable=False, default=False)
    bio_based = Column(Boolean, nullable=False, default=False)

    # Economics
    cost_index = Column(Float, nullable=False, default=0.5)  # 0=cheapest, 1=most expensive

    # Physical specs
    typical_thickness_min_um = Column(Float, nullable=True)  # micrometres
    typical_thickness_max_um = Column(Float, nullable=True)

    # Meta
    description = Column(Text, nullable=True)
    suitable_for = Column(Text, nullable=True)  # JSON array of food category strings

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    primary_recommendations = relationship(
        "Recommendation",
        back_populates="primary_material",
        foreign_keys="Recommendation.primary_material_id",
    )
