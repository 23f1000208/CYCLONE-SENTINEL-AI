import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, Optional, Union
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.core.config import settings

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DISASTER_MANAGER = "DISASTER_MANAGER"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    exp: Optional[int] = None

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token",
    auto_error=False
)

def get_password_hash(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations and random salt."""
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt and PBKDF2 hash."""
    try:
        salt_hex, key_hex = hashed_password.split("$")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        actual_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(expected_key, actual_key)
    except Exception:
        return False

def create_access_token(subject: Union[str, Any], role: UserRole = UserRole.VIEWER, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "role": role.value,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp())
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(allowed_roles: list[UserRole]):
    def role_checker(token: Optional[str] = Depends(oauth2_scheme)) -> TokenPayload:
        if not token:
            # For hackathon ease-of-use with anonymous read access, default to VIEWER
            if UserRole.VIEWER in allowed_roles:
                return TokenPayload(sub="anonymous", role=UserRole.VIEWER)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required for this operational action",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = decode_access_token(token)
        if payload.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of: {[r.value for r in allowed_roles]}. Current role: {payload.role.value}"
            )
        return payload
    return role_checker
