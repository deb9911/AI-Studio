from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    role: str
    typ: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ConfigOut(BaseModel):
    data: Dict[str, Any]

class ConfigUpdate(BaseModel):
    data: Dict[str, Any]

    