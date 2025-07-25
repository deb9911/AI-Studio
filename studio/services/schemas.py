from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

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

    