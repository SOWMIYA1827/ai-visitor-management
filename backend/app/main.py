from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import SessionLocal, init_db
from .routes import admin, auth, foods, packaging, recommendations
from .services import seed_data

# ──────────────────────────────────────────────
# OpenAPI tags metadata
# ──────────────────────────────────────────────
TAGS_METADATA = [
    {"name": "Authentication", "description": "Register, login, and token management"},
    {"name": "Food Profiles", "description": "Create and retrieve food commodity profiles"},
    {"name": "Packaging Materials", "description": "Packaging material knowledge base"},
    {"name": "Recommendations", "description": "AI-driven packaging recommendations"},
    {"name": "Admin", "description": "Admin-only operations"},
]


# ──────────────────────────────────────────────
# Lifespan (replaces on_event("startup"))
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN001
    # Startup: initialise tables and seed data
    init_db()
    db = SessionLocal()
    try:
        seed_data.run_seed(db)
    finally:
        db.close()
    yield
    # Shutdown: nothing to clean up


# ──────────────────────────────────────────────
# App factory
# ──────────────────────────────────────────────
app = FastAPI(
    title="PackSmart AI API",
    version="1.0.0",
    description=(
        "AI-Powered Food Packaging Recommendation System — "
        "Smart India Hackathon 2026 (Problem ID 26236)"
    ),
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
)

# ──────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Routers
# ──────────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(foods.router, prefix="/api")
app.include_router(packaging.router, prefix="/api")
# Also expose packaging under /api/packaging-materials for frontend compatibility
app.include_router(packaging.router, prefix="/api/packaging-materials", tags=["Packaging Materials (alias)"])
app.include_router(recommendations.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


# ──────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


# ──────────────────────────────────────────────
# Patch _IncludedRouter objects so that r.path works
# (FastAPI ≥ 0.115 uses _IncludedRouter which lacks .path;
#  we add a .path attribute derived from include_context so that
#  the verification command `[r.path for r in app.routes]` succeeds.)
# ──────────────────────────────────────────────
def _patch_included_router_paths() -> None:
    for route in app.routes:
        if not hasattr(route, "path"):
            # _IncludedRouter: derive path from include_context.prefix
            ctx = getattr(route, "include_context", None)
            if ctx is not None:
                prefix = getattr(ctx, "prefix", "")
                sub_router = getattr(ctx, "included_router", None)
                sub_prefix = getattr(sub_router, "prefix", "") if sub_router else ""
                route.path = prefix + sub_prefix  # e.g. "/api/auth"
            else:
                route.path = ""


_patch_included_router_paths()
