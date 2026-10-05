from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Build engine kwargs — check_same_thread is only valid for SQLite
_engine_kwargs: dict = {}
if settings.DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yield a DB session and close it on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined on Base.metadata."""
    # Import all models so their metadata is registered before create_all
    from .models import user, food, packaging, recommendation  # noqa: F401
    Base.metadata.create_all(bind=engine)
