from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserInDB

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def fake_hash_password(password: str):
    return "".join(a + b for a, b in zip(password, password[::1]))


fake_users_db = {"username": "alanv", "hashed_password": "steecrrceets"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
