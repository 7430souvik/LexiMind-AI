from fastapi import APIRouter, Depends,HTTPException, status
from app.auth.jwt import create_access_token
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import UserCreate, UserResponse, UserLogin,Token
from app.auth.hashing import verify_password
from app.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm


from app.services.user_service import (
    create_user,
    get_user_by_email,
)

router= APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register new User
    """

    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email already registered",
        )
    
    new_user = create_user(
        db,
        user
    )
    
    return new_user

@router.post(
    "/login",
    response_model= Token,
)

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session= Depends(get_db),
):
    # Step 1: Find the user by email
    db_user = get_user_by_email(
        db,
        form_data.username,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Step 3: Verify password
    if not verify_password(
        form_data.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # Step 4: Create JWT token
    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
        }
    )
    # Step 5: Return token
    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,

)

def get_me(
    current_user = Depends(get_current_user),
):
    return current_user

