from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session


from app.auth.jwt import verify_access_token
from app.database.session import get_db
from app.services.user_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
)

def get_current_user(
    token:str= Depends(oauth2_scheme),
    db:Session= Depends(get_db),
):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "could not validate credentials",
    )
    
    try:
        payload= verify_access_token(token)

        user_id= payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        user= get_user_by_id(
            db,
            int(user_id),
        )
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception