from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserCreate
from app.auth.hashing import hash_password


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Get a user by email.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )
    

def create_user(
        db:Session,
        user: UserCreate,
)->User:
    """
    Ceate a new user.
    """

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password= hash_password(
            user.password

        ),
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    """
    Get a user by ID.
    """

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    