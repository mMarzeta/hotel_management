from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False


class UserRegisterIn(BaseModel):
    username: str
    email: str
    full_name:str
    plain_password: str
    pesel: str
    address: str
    tel_number: str


class UserRegisterOut(User):
    full_name: str
    email: str
    id: str


class UserInDB(User):
    hashed_password: str
    id: str


class UserDetails(User):
    id: str
    pesel: str
    address: str
    tel_number: str
