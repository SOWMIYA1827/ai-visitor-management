"""
Authentication service — business logic for user management.
"""
from typing import Optional

from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.auth import UserCreate
from ..utils.auth import get_password_hash, verify_password


class AuthService:
    """Stateless service class; all methods take a db session as first arg."""

    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        """
        Create a new user row.

        Raises
        ------
        ValueError
            If a user with the same email already exists.
        """
        existing = db.query(User).filter(User.email == user_create.email).first()
        if existing:
            raise ValueError(f"Email '{user_create.email}' is already registered.")

        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            user_type=user_create.user_type,
            organization=user_create.organization,
            phone_number=user_create.phone_number,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Verify credentials and return the User, or None on failure.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        return db.query(User).order_by(User.created_at.desc()).all()

    @staticmethod
    def update_user_status(db: Session, user_id: str, is_active: bool) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user
