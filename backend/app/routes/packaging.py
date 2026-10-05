"""Packaging material routes — implemented in FEAT-002."""
from fastapi import APIRouter

router = APIRouter(prefix="/packaging", tags=["Packaging Materials"])
