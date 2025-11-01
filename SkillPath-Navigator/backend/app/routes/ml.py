from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import httpx

from ..models import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItem,
    LearningPathResponse,
    LearningPathNode,
    SkillGapAnalysis,
    JobMarketInsight,
    NSQFLevel
)
from ..auth import get_current_user, TokenData
from ..utils.db import get_db, UserDB, LearnerProfileDB, CourseDB, JobMarketDataDB

router = APIRouter(prefix="/api/ml", tags=["machine-learning"])

ML_SERVICE_URL = "http://localhost:8001"


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    top_k: int = Query(default=10, ge=1, le=50),
    include_explanations: bool = Query(default=True),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized course recommendations for the current user."""
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
            detail="Learner profile not found. Please complete your profile first."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ML_SERVICE_URL}/recommend",
                json={
                    "learner_id": user.id,
                    "education_level": profile.education_level,
                    "prior_skills": profile.prior_skills,
                    "career_aspirations": profile.career_aspirations,
                    "interests": profile.interests,
                    "top_k": top_k,
                    "include_explanations": include_explanations
                },
                timeout=30.0
            )
            response.raise_for_status()
            ml_recommendations = response.json()
    except httpx.HTTPError:
        courses = db.query(CourseDB).filter(CourseDB.is_active == True).limit(top_k).all()
        
        recommendations = []
        for course in courses:
            recommendations.append(
                RecommendationItem(
                    course_id=course.id,
                    course_title=course.title,
                    nsqf_level=NSQFLevel(course.nsqf_level),
                    sector=course.sector,
                    relevance_score=0.75,
                    explanation="Recommended based on your profile" if include_explanations else None,
                    estimated_duration_hours=course.duration_hours,
                    skills_to_gain=course.skills_covered
                )
            )
        
        return RecommendationResponse(
            learner_id=user.id,
            recommendations=recommendations,
            generated_at=datetime.utcnow(),
            model_version="1.0.0-fallback"
        )
    
    course_ids = [rec["course_id"] for rec in ml_recommendations.get("recommendations", [])]
    courses = db.query(CourseDB).filter(CourseDB.id.in_(course_ids)).all()
    course_map = {course.id: course for course in courses}
    
    recommendations = []
    for rec in ml_recommendations.get("recommendations", []):
        course = course_map.get(rec["course_id"])
        if course:
            recommendations.append(
                RecommendationItem(
                    course_id=course.id,
                    course_title=course.title,
                    nsqf_level=NSQFLevel(course.nsqf_level),
                    sector=course.sector,
                    relevance_score=rec.get("relevance_score", 0.5),
                    explanation=rec.get("explanation") if include_explanations else None,
                    estimated_duration_hours=course.duration_hours,
                    skills_to_gain=course.skills_covered
                )
            )
    
    return RecommendationResponse(
        learner_id=user.id,
        recommendations=recommendations,
        generated_at=datetime.utcnow(),
        model_version=ml_recommendations.get("model_version", "1.0.0")
    )


@router.get("/learning-path", response_model=LearningPathResponse)
async def get_learning_path(
    career_goal: str = Query(..., description="Target career goal"),
    target_nsqf_level: Optional[NSQFLevel] = Query(None),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a personalized learning path to achieve a career goal."""
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
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ML_SERVICE_URL}/learning-path",
                json={
                    "learner_id": user.id,
                    "career_goal": career_goal,
                    "target_nsqf_level": target_nsqf_level,
                    "current_skills": profile.prior_skills,
                    "education_level": profile.education_level
                },
                timeout=30.0
            )
            response.raise_for_status()
            path_data = response.json()
    except httpx.HTTPError:
        courses = db.query(CourseDB).filter(CourseDB.is_active == True).limit(5).all()
        
        path_nodes = []
        for idx, course in enumerate(courses):
            path_nodes.append(
                LearningPathNode(
                    course_id=course.id,
                    course_title=course.title,
                    nsqf_level=NSQFLevel(course.nsqf_level),
                    sequence_order=idx + 1,
                    estimated_completion_weeks=course.duration_hours // 10,
                    prerequisites_met=True
                )
            )
        
        total_weeks = sum(node.estimated_completion_weeks for node in path_nodes)
        
        return LearningPathResponse(
            learner_id=user.id,
            path_nodes=path_nodes,
            total_duration_weeks=total_weeks,
            target_nsqf_level=target_nsqf_level or NSQFLevel.LEVEL_5,
            career_goal=career_goal,
            generated_at=datetime.utcnow()
        )
    
    course_ids = [node["course_id"] for node in path_data.get("path_nodes", [])]
    courses = db.query(CourseDB).filter(CourseDB.id.in_(course_ids)).all()
    course_map = {course.id: course for course in courses}
    
    path_nodes = []
    for node in path_data.get("path_nodes", []):
        course = course_map.get(node["course_id"])
        if course:
            path_nodes.append(
                LearningPathNode(
                    course_id=course.id,
                    course_title=course.title,
                    nsqf_level=NSQFLevel(course.nsqf_level),
                    sequence_order=node.get("sequence_order", 0),
                    estimated_completion_weeks=node.get("estimated_completion_weeks", 4),
                    prerequisites_met=node.get("prerequisites_met", True)
                )
            )
    
    return LearningPathResponse(
        learner_id=user.id,
        path_nodes=path_nodes,
        total_duration_weeks=path_data.get("total_duration_weeks", 0),
        target_nsqf_level=NSQFLevel(path_data.get("target_nsqf_level", "5")),
        career_goal=career_goal,
        generated_at=datetime.utcnow()
    )


@router.get("/skill-gap-analysis", response_model=SkillGapAnalysis)
async def analyze_skill_gap(
    target_role: str = Query(..., description="Target job role"),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze skill gaps for a target role."""
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
    
    required_skills = ["Python", "Data Analysis", "Machine Learning", "SQL", "Communication"]
    skill_gaps = [skill for skill in required_skills if skill not in profile.prior_skills]
    
    relevant_courses = db.query(CourseDB).filter(CourseDB.is_active == True).limit(3).all()
    recommended_course_ids = [course.id for course in relevant_courses]
    
    return SkillGapAnalysis(
        learner_id=user.id,
        current_skills=profile.prior_skills,
        target_role=target_role,
        required_skills=required_skills,
        skill_gaps=skill_gaps,
        recommended_courses=recommended_course_ids,
        estimated_upskilling_weeks=len(skill_gaps) * 4
    )


@router.get("/job-market-insights", response_model=List[JobMarketInsight])
async def get_job_market_insights(
    skills: Optional[List[str]] = Query(None),
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get job market insights for specific skills or sectors."""
    query = db.query(JobMarketDataDB)
    
    if skills:
        query = query.filter(JobMarketDataDB.skill_name.in_(skills))
    
    market_data = query.limit(20).all()
    
    insights = []
    for data in market_data:
        insights.append(
            JobMarketInsight(
                skill_name=data.skill_name,
                demand_score=data.demand_score,
                growth_trend=data.growth_trend,
                avg_salary_range=data.avg_salary_range,
                top_industries=data.top_industries,
                related_courses=data.related_courses
            )
        )
    
    return insights
