# studio/services/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict
import jwt as pyjwt
from passlib.context import CryptContext
from studio.settings import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def _create_token(subject: str | int, expires_delta: timedelta, extra: Dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        **extra,
    }
    return pyjwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int, role: str, minutes: int) -> str:
    return _create_token(user_id, timedelta(minutes=minutes), {"role": role, "typ": "access"})

def create_refresh_token(user_id: int, role: str, days: int) -> str:
    return _create_token(user_id, timedelta(days=days), {"role": role, "typ": "refresh"})

def decode_token(token: str) -> dict:
    return pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
