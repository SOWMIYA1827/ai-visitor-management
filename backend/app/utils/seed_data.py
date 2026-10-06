"""
Re-export shim so both import paths work:
  from app.utils.seed_data import run_seed
  from app.services.seed_data import run_seed
"""
from ..services.seed_data import run_seed  # noqa: F401

__all__ = ["run_seed"]
