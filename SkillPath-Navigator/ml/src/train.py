import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
import joblib
import json
import os
from typing import Dict, Any, List


class LearnerProfileModel:
    """Model for learner profiling and skill prediction."""
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.skill_encoder = {}
        self.education_encoder = {
            "below_10th": 1,
            "10th": 2,
            "12th": 3,
            "diploma": 4,
            "graduate": 5,
            "post_graduate": 6,
            "doctorate": 7
        }
    
    def prepare_features(self, learner_data: pd.DataFrame) -> np.ndarray:
        """Prepare features from learner data."""
        features = []
        
        for _, row in learner_data.iterrows():
            feature_vector = [
                self.education_encoder.get(row.get("education_level", "graduate"), 5),
                row.get("age", 25),
                row.get("work_experience_years", 0),
                len(row.get("prior_skills", [])),
                len(row.get("career_aspirations", [])),
                len(row.get("interests", []))
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train(self, training_data: pd.DataFrame, target_column: str = "success_score"):
        """Train the learner profiling model."""
        X = self.prepare_features(training_data)
        y = training_data[target_column].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = LGBMClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Training accuracy: {train_score:.4f}")
        print(f"Testing accuracy: {test_score:.4f}")
        
        return {
            "train_score": train_score,
            "test_score": test_score
        }
    
    def predict_success_probability(self, learner_data: Dict[str, Any]) -> float:
        """Predict success probability for a learner."""
        if self.model is None:
            return 0.75
        
        df = pd.DataFrame([learner_data])
        features = self.prepare_features(df)
        
        probabilities = self.model.predict_proba(features)
        return float(probabilities[0][1])
    
    def save_model(self, path: str):
        """Save trained model to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            "model": self.model,
            "feature_names": self.feature_names,
            "skill_encoder": self.skill_encoder,
            "education_encoder": self.education_encoder
        }, path)
        print(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model from disk."""
        data = joblib.load(path)
        self.model = data["model"]
        self.feature_names = data["feature_names"]
        self.skill_encoder = data["skill_encoder"]
        self.education_encoder = data["education_encoder"]
        print(f"Model loaded from {path}")


class SkillMatchingModel:
    """Model for matching learner skills with job requirements."""
    
    def __init__(self):
        self.skill_job_matrix = {}
        self.job_skill_requirements = {}
    
    def build_skill_job_matrix(self, job_market_data: pd.DataFrame):
        """Build skill-job matching matrix."""
        for _, row in job_market_data.iterrows():
            skill = row["skill_name"]
            demand_score = row["demand_score"]
            industries = row.get("top_industries", [])
            
            self.skill_job_matrix[skill] = {
                "demand_score": demand_score,
                "industries": industries,
                "growth_trend": row.get("growth_trend", "stable")
            }
    
    def match_skills_to_jobs(
        self,
        learner_skills: List[str],
        target_role: str
    ) -> Dict[str, Any]:
        """Match learner skills to job requirements."""
        required_skills = self.job_skill_requirements.get(
            target_role,
            ["Python", "Data Analysis", "Communication", "Problem Solving"]
        )
        
        matched_skills = set(learner_skills) & set(required_skills)
        missing_skills = set(required_skills) - set(learner_skills)
        
        match_score = len(matched_skills) / len(required_skills) if required_skills else 0
        
        return {
            "match_score": match_score,
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "required_skills": required_skills
        }
    
    def save_model(self, path: str):
        """Save skill matching data."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            "skill_job_matrix": self.skill_job_matrix,
            "job_skill_requirements": self.job_skill_requirements
        }, path)
        print(f"Skill matching model saved to {path}")


def generate_synthetic_training_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate synthetic training data for model development."""
    np.random.seed(42)
    
    education_levels = ["10th", "12th", "diploma", "graduate", "post_graduate"]
    skills_pool = [
        "Python", "Java", "JavaScript", "Data Analysis", "Machine Learning",
        "SQL", "Communication", "Leadership", "Project Management", "Excel"
    ]
    
    data = []
    for i in range(n_samples):
        n_skills = np.random.randint(1, 6)
        prior_skills = np.random.choice(skills_pool, n_skills, replace=False).tolist()
        
        age = np.random.randint(18, 50)
        work_exp = min(age - 18, np.random.randint(0, 15))
        
        success_score = (
            len(prior_skills) * 0.2 +
            (age - 18) * 0.01 +
            work_exp * 0.05 +
            np.random.random() * 0.3
        )
        success_label = 1 if success_score > 0.5 else 0
        
        data.append({
            "learner_id": i + 1,
            "education_level": np.random.choice(education_levels),
            "prior_skills": prior_skills,
            "career_aspirations": ["Data Scientist", "Software Engineer"],
            "interests": ["Technology", "Innovation"],
            "age": age,
            "work_experience_years": work_exp,
            "success_score": success_label
        })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Generating synthetic training data...")
    training_data = generate_synthetic_training_data(1000)
    
    print("\nTraining learner profile model...")
    profile_model = LearnerProfileModel()
    metrics = profile_model.train(training_data)
    
    model_dir = "../models"
    os.makedirs(model_dir, exist_ok=True)
    
    profile_model.save_model(f"{model_dir}/learner_profile_model.pkl")
    
    print("\nTraining complete!")
    print(f"Model metrics: {json.dumps(metrics, indent=2)}")
