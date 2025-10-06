from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import secrets

# Simple in-memory token store (in production, use Redis or JWT)
active_tokens = {}

security = HTTPBearer()


def create_token(user_id: int) -> str:
    """Create a simple token for the user"""
    token = secrets.token_urlsafe(32)
    active_tokens[token] = user_id
    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Verify token and return current authenticated user"""
    token = credentials.credentials
    user_id = active_tokens.get(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

