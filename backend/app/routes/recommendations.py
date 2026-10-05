"""Recommendation routes — implemented in FEAT-003."""
from fastapi import APIRouter

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
