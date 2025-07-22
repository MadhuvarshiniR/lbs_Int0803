from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import crud, schemas, security
from .database import get_db_connection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = security.verify_token(token, credentials_exception)
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_librarian(current_user: schemas.User = Depends(get_current_user)):
    if current_user['role'] != "librarian":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
