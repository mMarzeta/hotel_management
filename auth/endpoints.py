from datetime import timedelta

from fastapi import Depends, HTTPException, FastAPI, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from oauth2 import authenticate_user, create_access_token, get_current_active_user
from schemas import Token, User, UserRegisterIn, UserDetails
from oauth2 import register_user as oauth_register_user

app = FastAPI()


@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserDetails)
async def read_users_me(current_user: UserDetails = Depends(get_current_active_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "disabled": current_user.disabled,
        "pesel": current_user.pesel,
        "address": current_user.address,
        "tel_number": current_user.tel_number
    }


@app.post("/register")
async def register_user(*, user: UserRegisterIn):
    user_id = await oauth_register_user(user)
    return {
        "username": user.username,
        "email": user.email,
        "id": user_id
    }
