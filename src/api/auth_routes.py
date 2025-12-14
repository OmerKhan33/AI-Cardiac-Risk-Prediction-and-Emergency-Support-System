from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from pydantic import BaseModel
from src.db.database import get_session
from src.models.user_model import User
from src.auth.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
import os

router = APIRouter(tags=["Authentication"])

class UserCreate(BaseModel):
    username: str
    password: str  # Plain text input
    role: str = "user"

@router.post("/register", status_code=201)
def register(user_input: UserCreate, session: Session = Depends(get_session)): # 👈 Use UserCreate here
    
    # 2. Check if user already exists
    existing_user = session.query(User).filter(User.username == user_input.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # 3. Hash the password (We take the PLAIN password and hash it)
    hashed_pwd = get_password_hash(user_input.password)
    
    # 4. Create the Database User
    new_user = User(
        username=user_input.username,
        hashed_password=hashed_pwd, # Store the hash
        role=user_input.role
    )
    
    # 5. Save to DB
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": f"User {new_user.username} created successfully"}
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # 1. Find user
    user = session.query(User).filter(User.username == form_data.username).first()
    
    # 2. Check password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Create Token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}