import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_bearer = HTTPBearer()

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> Dict:
    """
    Decodes the JWT token to extract the user information for RBAC.
    """
    token = credentials.credentials
    user = decode_access_token(token)
    return user

def require_role(required_role: str):
    """
    Dependency generator for RBAC.
    """
    def role_checker(user: Dict = Security(get_current_user)):
        roles = user.get("roles", [])
        if required_role not in roles and "admin" not in roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker
