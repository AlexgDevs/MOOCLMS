from . import BaseModel


class RegisterUser(BaseModel):
    name: str
    password: str


class LoginUser(BaseModel):
    name: str
    password: str