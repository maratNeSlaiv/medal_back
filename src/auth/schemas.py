# auth/schemas.py
from pydantic import BaseModel

class RegisterModel(BaseModel):
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str
