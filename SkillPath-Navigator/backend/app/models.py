from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class NSQFLevel(str, Enum):
    LEVEL_1 = "1"
    LEVEL_2 = "2"
    LEVEL_3 = "3"
    LEVEL_4 = "4"
    LEVEL_5 = "5"
    LEVEL_6 = "6"
    LEVEL_7 = "7"
    LEVEL_8 = "8"
    LEVEL_9 = "9"
    LEVEL_10 = "10"


class EducationLevel(str, Enum):
    BELOW_10TH = "below_10th"
    CLASS_10TH = "10th"
    CLASS_12TH = "12th"
    DIPLOMA = "diploma"
    GRADUATE = "graduate"
    POST_GRADUATE = "post_graduate"
    DOCTORATE = "doctorate"


class SocioEconomicStatus(str, Enum):
    BPL = "bpl"
    APL = "apl"
    MIDDLE_CLASS = "middle_class"
    UPPER_MIDDLE = "upper_middle"


class LearningPace(str, Enum):
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    preferred_language: str = "en"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class LearnerProfileBase(BaseModel):
    user_id: int
    education_level: EducationLevel
    prior_skills: List[str] = Field(default_factory=list)
    career_aspirations: List[str] = Field(default_factory=list)
    socio_economic_status: Optional[SocioEconomicStatus] = None
    learning_pace: LearningPace = LearningPace.MODERATE
    location: Optional[str] = None
    age: Optional[int] = Field(None, ge=15, le=100)
    work_experience_years: Optional[int] = Field(None, ge=0, le=50)
    current_occupation: Optional[str] = None
    interests: List[str] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)


class LearnerProfileCreate(LearnerProfileBase):
    pass


class LearnerProfile(LearnerProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    description: str
    nsqf_level: NSQFLevel
    sector: str
    duration_hours: int
    skills_covered: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    certification_body: Optional[str] = None
    is_active: bool = True


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    learner_id: int
    top_k: int = Field(default=10, ge=1, le=50)
    include_explanations: bool = True


class RecommendationItem(BaseModel):
    course_id: int
    course_title: str
    nsqf_level: NSQFLevel
    sector: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    explanation: Optional[str] = None
    estimated_duration_hours: int
    skills_to_gain: List[str]


class RecommendationResponse(BaseModel):
    learner_id: int
    recommendations: List[RecommendationItem]
    generated_at: datetime
    model_version: str = "1.0.0"


class LearningPathNode(BaseModel):
    course_id: int
    course_title: str
    nsqf_level: NSQFLevel
    sequence_order: int
    estimated_completion_weeks: int
    prerequisites_met: bool = True


class LearningPathResponse(BaseModel):
    learner_id: int
    path_nodes: List[LearningPathNode]
    total_duration_weeks: int
    target_nsqf_level: NSQFLevel
    career_goal: str
    generated_at: datetime


class ProgressUpdate(BaseModel):
    learner_id: int
    course_id: int
    completion_percentage: float = Field(..., ge=0.0, le=100.0)
    skills_acquired: List[str] = Field(default_factory=list)
    assessment_score: Optional[float] = Field(None, ge=0.0, le=100.0)


class ProgressRecord(ProgressUpdate):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobMarketInsight(BaseModel):
    skill_name: str
    demand_score: float = Field(..., ge=0.0, le=1.0)
    growth_trend: str
    avg_salary_range: Optional[str] = None
    top_industries: List[str] = Field(default_factory=list)
    related_courses: List[int] = Field(default_factory=list)


class SkillGapAnalysis(BaseModel):
    learner_id: int
    current_skills: List[str]
    target_role: str
    required_skills: List[str]
    skill_gaps: List[str]
    recommended_courses: List[int]
    estimated_upskilling_weeks: int
