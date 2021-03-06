import logging
import uuid
from datetime import datetime, timedelta

import jwt
import peewee
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

from config import SECRET_KEY, ALGORITHM
from models import UserModel
from schemas import TokenData, UserRegisterIn, UserDetails

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        logging.error(e)
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = UserModel.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = UserModel.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserDetails = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def register_user(user: UserRegisterIn):
    try:
        user_id = str(uuid.uuid4())
        UserModel.create(
            id=user_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            pesel=user.pesel,
            address=user.address,
            tel_number=user.tel_number,
            hashed_password=get_password_hash(user.plain_password),
            disabled=False,
        )
        logging.info(f"Created user {user.username}")
        return user_id
    except peewee.IntegrityError as e:
        logging.error(e)
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User with given username already exists."
        )
