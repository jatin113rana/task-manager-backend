from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------------------
# Pydantic Models
# ---------------------------
class RegisterRequest(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    role: str = Field(..., min_length=3, max_length=50)

class LoginRequest(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class AuthResponse(BaseModel):
    message: str
    user_id: int = None  # Optional for login

# ---------------------------
# Register Route
# ---------------------------
@router.post("/register", response_model=AuthResponse)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with username, password, and role.
    """
    # Check if username already exists
    if db.query(User).filter(User.user_name == request.user_name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Check if password and confirm_password match
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Hash the password
    hashed_pwd = hash_password(request.password)

    # Create new user
    new_user = User(
        user_name=request.user_name,
        role=request.role,
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.user_id}

# ---------------------------
# Login Route
# ---------------------------
@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == request.user_name).first()

    if not user or not verify_password(request.password, user.password):
        return {"message": "Invalid Credentials","error":True}

    return {"message": "Login successful", "user_id": user.user_id,"role":user.role,"error":False}
