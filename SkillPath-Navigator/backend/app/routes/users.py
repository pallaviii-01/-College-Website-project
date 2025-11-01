from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from ..models import UserCreate, User, UserLogin, Token, LearnerProfileCreate, LearnerProfile
from ..auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TokenData
)
from ..utils.db import get_db, UserDB, LearnerProfileDB

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = UserDB(
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        preferred_language=user.preferred_language,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return User(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        phone=new_user.phone,
        preferred_language=new_user.preferred_language,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = db.query(UserDB).filter(UserDB.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current authenticated user information."""
    user = db.query(UserDB).filter(UserDB.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        preferred_language=user.preferred_language,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.post("/profile", response_model=LearnerProfile, status_code=status.HTTP_201_CREATED)
async def create_learner_profile(
    profile: LearnerProfileCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update learner profile."""
    user = db.query(UserDB).filter(UserDB.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    existing_profile = db.query(LearnerProfileDB).filter(
        LearnerProfileDB.user_id == user.id
    ).first()
    
    if existing_profile:
        existing_profile.education_level = profile.education_level
        existing_profile.prior_skills = profile.prior_skills
        existing_profile.career_aspirations = profile.career_aspirations
        existing_profile.socio_economic_status = profile.socio_economic_status
        existing_profile.learning_pace = profile.learning_pace
        existing_profile.location = profile.location
        existing_profile.age = profile.age
        existing_profile.work_experience_years = profile.work_experience_years
        existing_profile.current_occupation = profile.current_occupation
        existing_profile.interests = profile.interests
        existing_profile.constraints = profile.constraints
        db.commit()
        db.refresh(existing_profile)
        db_profile = existing_profile
    else:
        new_profile = LearnerProfileDB(
            user_id=user.id,
            education_level=profile.education_level,
            prior_skills=profile.prior_skills,
            career_aspirations=profile.career_aspirations,
            socio_economic_status=profile.socio_economic_status,
            learning_pace=profile.learning_pace,
            location=profile.location,
            age=profile.age,
            work_experience_years=profile.work_experience_years,
            current_occupation=profile.current_occupation,
            interests=profile.interests,
            constraints=profile.constraints
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        db_profile = new_profile
    
    return LearnerProfile(
        id=db_profile.id,
        user_id=db_profile.user_id,
        education_level=db_profile.education_level,
        prior_skills=db_profile.prior_skills,
        career_aspirations=db_profile.career_aspirations,
        socio_economic_status=db_profile.socio_economic_status,
        learning_pace=db_profile.learning_pace,
        location=db_profile.location,
        age=db_profile.age,
        work_experience_years=db_profile.work_experience_years,
        current_occupation=db_profile.current_occupation,
        interests=db_profile.interests,
        constraints=db_profile.constraints,
        created_at=db_profile.created_at,
        updated_at=db_profile.updated_at
    )


@router.get("/profile", response_model=LearnerProfile)
async def get_learner_profile(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learner profile for current user."""
    user = db.query(UserDB).filter(UserDB.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    profile = db.query(LearnerProfileDB).filter(
        LearnerProfileDB.user_id == user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner profile not found"
        )
    
    return LearnerProfile(
        id=profile.id,
        user_id=profile.user_id,
        education_level=profile.education_level,
        prior_skills=profile.prior_skills,
        career_aspirations=profile.career_aspirations,
        socio_economic_status=profile.socio_economic_status,
        learning_pace=profile.learning_pace,
        location=profile.location,
        age=profile.age,
        work_experience_years=profile.work_experience_years,
        current_occupation=profile.current_occupation,
        interests=profile.interests,
        constraints=profile.constraints,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )
