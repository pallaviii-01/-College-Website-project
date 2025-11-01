from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn

from recommend import RecommendationEngine

app = FastAPI(
    title="SkillPath ML Service",
    description="Machine Learning service for personalized recommendations",
    version="1.0.0"
)

recommendation_engine = RecommendationEngine()


class RecommendationRequest(BaseModel):
    learner_id: int
    education_level: str
    prior_skills: List[str] = Field(default_factory=list)
    career_aspirations: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    top_k: int = Field(default=10, ge=1, le=50)
    include_explanations: bool = True


class LearningPathRequest(BaseModel):
    learner_id: int
    career_goal: str
    target_nsqf_level: Optional[str] = None
    current_skills: List[str] = Field(default_factory=list)
    education_level: str


@app.get("/")
async def root():
    return {
        "service": "SkillPath ML Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    """Generate personalized course recommendations."""
    try:
        learner_data = {
            "learner_id": request.learner_id,
            "education_level": request.education_level,
            "prior_skills": request.prior_skills,
            "career_aspirations": request.career_aspirations,
            "interests": request.interests
        }
        
        recommendations = recommendation_engine.recommend(
            learner_data,
            top_k=request.top_k,
            include_explanations=request.include_explanations
        )
        
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/learning-path")
async def generate_learning_path(request: LearningPathRequest):
    """Generate a personalized learning path."""
    try:
        learner_data = {
            "learner_id": request.learner_id,
            "education_level": request.education_level,
            "prior_skills": request.current_skills
        }
        
        path = recommendation_engine.generate_learning_path(
            learner_data,
            career_goal=request.career_goal,
            target_nsqf_level=request.target_nsqf_level
        )
        
        return path
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/skill-match")
async def match_skills(
    learner_skills: List[str],
    target_role: str
):
    """Match learner skills with job requirements."""
    required_skills = {
        "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
        "Software Engineer": ["Programming", "Data Structures", "Algorithms", "System Design"],
        "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "Digital Marketer": ["SEO", "Content Marketing", "Social Media", "Analytics"]
    }
    
    role_skills = required_skills.get(target_role, ["Communication", "Problem Solving"])
    matched = set(learner_skills) & set(role_skills)
    missing = set(role_skills) - set(learner_skills)
    
    return {
        "match_score": len(matched) / len(role_skills) if role_skills else 0,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "required_skills": role_skills
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
