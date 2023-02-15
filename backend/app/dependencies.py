from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import models
from .schemas import User
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def decode_token(token: str):
    return User(username="SomeUser")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
