import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import json
import os


class RecommendationEngine:
    """Hybrid recommendation engine combining content-based and collaborative filtering."""
    
    def __init__(self, model_path: str = "../models"):
        self.model_path = model_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.course_embeddings = None
        self.courses_df = None
        self.skill_synonyms = {}
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models and data."""
        try:
            courses_path = os.path.join(self.model_path, "courses_embeddings.pkl")
            if os.path.exists(courses_path):
                data = joblib.load(courses_path)
                self.course_embeddings = data['embeddings']
                self.courses_df = data['courses']
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
    
    def normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize skill names using synonyms."""
        normalized = []
        for skill in skills:
            skill_lower = skill.lower().strip()
            normalized.append(self.skill_synonyms.get(skill_lower, skill))
        return normalized
    
    def compute_learner_profile_embedding(self, learner_data: Dict[str, Any]) -> np.ndarray:
        """Compute embedding for learner profile."""
        profile_text = " ".join([
            " ".join(learner_data.get("prior_skills", [])),
            " ".join(learner_data.get("career_aspirations", [])),
            " ".join(learner_data.get("interests", [])),
            learner_data.get("education_level", ""),
            learner_data.get("current_occupation", "")
        ])
        
        return self.embedding_model.encode(profile_text, convert_to_tensor=False)
    
    def content_based_recommendations(
        self,
        learner_embedding: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate content-based recommendations."""
        if self.course_embeddings is None or self.courses_df is None:
            return []
        
        similarities = cosine_similarity([learner_embedding], self.course_embeddings)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k * 2]
        
        recommendations = []
        for idx in top_indices:
            if len(recommendations) >= top_k:
                break
            
            course = self.courses_df.iloc[idx]
            
            if filters:
                if filters.get("nsqf_level") and course.get("nsqf_level") != filters["nsqf_level"]:
                    continue
                if filters.get("sector") and course.get("sector") != filters["sector"]:
                    continue
            
            recommendations.append({
                "course_id": int(course["id"]),
                "relevance_score": float(similarities[idx]),
                "explanation": self._generate_explanation(course, similarities[idx])
            })
        
        return recommendations
    
    def _generate_explanation(self, course: pd.Series, score: float) -> str:
        """Generate human-readable explanation for recommendation."""
        reasons = []
        
        if score > 0.8:
            reasons.append("Highly aligned with your profile")
        elif score > 0.6:
            reasons.append("Good match for your skills and interests")
        else:
            reasons.append("Relevant to your career goals")
        
        if course.get("skills_covered"):
            skills = course["skills_covered"][:3] if isinstance(course["skills_covered"], list) else []
            if skills:
                reasons.append(f"Covers: {', '.join(skills)}")
        
        return ". ".join(reasons)
    
    def recommend(
        self,
        learner_data: Dict[str, Any],
        top_k: int = 10,
        include_explanations: bool = True
    ) -> Dict[str, Any]:
        """Generate personalized recommendations."""
        learner_embedding = self.compute_learner_profile_embedding(learner_data)
        
        recommendations = self.content_based_recommendations(
            learner_embedding,
            top_k=top_k
        )
        
        if not include_explanations:
            for rec in recommendations:
                rec.pop("explanation", None)
        
        return {
            "recommendations": recommendations,
            "model_version": "1.0.0"
        }
    
    def generate_learning_path(
        self,
        learner_data: Dict[str, Any],
        career_goal: str,
        target_nsqf_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a sequential learning path."""
        current_skills = set(learner_data.get("prior_skills", []))
        
        if self.courses_df is None:
            return {
                "path_nodes": [],
                "total_duration_weeks": 0,
                "target_nsqf_level": target_nsqf_level or "5"
            }
        
        available_courses = self.courses_df.copy()
        
        if target_nsqf_level:
            available_courses = available_courses[
                available_courses["nsqf_level"] <= int(target_nsqf_level)
            ]
        
        path_nodes = []
        sequence_order = 1
        total_weeks = 0
        
        for _ in range(min(5, len(available_courses))):
            eligible_courses = []
            
            for idx, course in available_courses.iterrows():
                prerequisites = set(course.get("prerequisites", []))
                if prerequisites.issubset(current_skills):
                    eligible_courses.append((idx, course))
            
            if not eligible_courses:
                break
            
            best_idx, best_course = eligible_courses[0]
            
            duration_weeks = best_course.get("duration_hours", 40) // 10
            
            path_nodes.append({
                "course_id": int(best_course["id"]),
                "sequence_order": sequence_order,
                "estimated_completion_weeks": duration_weeks,
                "prerequisites_met": True
            })
            
            current_skills.update(best_course.get("skills_covered", []))
            available_courses = available_courses.drop(best_idx)
            sequence_order += 1
            total_weeks += duration_weeks
        
        return {
            "path_nodes": path_nodes,
            "total_duration_weeks": total_weeks,
            "target_nsqf_level": target_nsqf_level or "5"
        }


def create_dummy_course_embeddings(courses_data: List[Dict[str, Any]], output_path: str):
    """Create and save course embeddings."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    courses_df = pd.DataFrame(courses_data)
    
    course_texts = []
    for _, course in courses_df.iterrows():
        text = f"{course['title']} {course['description']} {' '.join(course.get('skills_covered', []))}"
        course_texts.append(text)
    
    embeddings = model.encode(course_texts, convert_to_tensor=False)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump({
        'embeddings': embeddings,
        'courses': courses_df
    }, output_path)
    
    print(f"Saved course embeddings to {output_path}")


if __name__ == "__main__":
    engine = RecommendationEngine()
    
    sample_learner = {
        "learner_id": 1,
        "education_level": "graduate",
        "prior_skills": ["Python", "Data Analysis"],
        "career_aspirations": ["Data Scientist", "ML Engineer"],
        "interests": ["Machine Learning", "AI"]
    }
    
    recommendations = engine.recommend(sample_learner, top_k=5)
    print(json.dumps(recommendations, indent=2))
