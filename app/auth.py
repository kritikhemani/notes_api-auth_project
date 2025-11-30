from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserRead, Token
from app.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/register", response_model=UserRead)  
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user