"""Authentication routes — implemented in FEAT-002."""
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])
