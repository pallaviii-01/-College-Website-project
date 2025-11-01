from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/skillpath_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    preferred_language = Column(String, default="en")
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    learner_profile = relationship("LearnerProfileDB", back_populates="user", uselist=False)
    progress_records = relationship("ProgressRecordDB", back_populates="user")


class LearnerProfileDB(Base):
    __tablename__ = "learner_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    education_level = Column(String, nullable=False)
    prior_skills = Column(JSON, default=list)
    career_aspirations = Column(JSON, default=list)
    socio_economic_status = Column(String, nullable=True)
    learning_pace = Column(String, default="moderate")
    location = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    work_experience_years = Column(Integer, nullable=True)
    current_occupation = Column(String, nullable=True)
    interests = Column(JSON, default=list)
    constraints = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserDB", back_populates="learner_profile")


class CourseDB(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    nsqf_level = Column(String, nullable=False, index=True)
    sector = Column(String, nullable=False, index=True)
    duration_hours = Column(Integer, nullable=False)
    skills_covered = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    certification_body = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    progress_records = relationship("ProgressRecordDB", back_populates="course")


class ProgressRecordDB(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completion_percentage = Column(Float, default=0.0)
    skills_acquired = Column(JSON, default=list)
    assessment_score = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserDB", back_populates="progress_records")
    course = relationship("CourseDB", back_populates="progress_records")


class JobMarketDataDB(Base):
    __tablename__ = "job_market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, index=True)
    demand_score = Column(Float, nullable=False)
    growth_trend = Column(String, nullable=False)
    avg_salary_range = Column(String, nullable=True)
    top_industries = Column(JSON, default=list)
    related_courses = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
