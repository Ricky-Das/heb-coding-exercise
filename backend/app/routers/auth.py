from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse
from app.auth import create_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with PIN"""
    user = db.query(User).filter(User.pin == request.pin).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    token = create_token(user.id)
    
    return LoginResponse(token=token, user_id=user.id, name=user.name)

