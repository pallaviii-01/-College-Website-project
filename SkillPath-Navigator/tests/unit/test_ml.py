import pytest
import numpy as np
import pandas as pd
from ml.src.recommend import RecommendationEngine
from ml.src.train import LearnerProfileModel, generate_synthetic_training_data


def test_recommendation_engine_initialization():
    """Test recommendation engine can be initialized."""
    engine = RecommendationEngine()
    assert engine is not None
    assert engine.embedding_model is not None


def test_learner_profile_embedding():
    """Test learner profile embedding generation."""
    engine = RecommendationEngine()
    
    learner_data = {
        "prior_skills": ["Python", "Data Analysis"],
        "career_aspirations": ["Data Scientist"],
        "interests": ["Machine Learning"],
        "education_level": "graduate",
        "current_occupation": "Student"
    }
    
    embedding = engine.compute_learner_profile_embedding(learner_data)
    
    assert embedding is not None
    assert isinstance(embedding, np.ndarray)
    assert len(embedding) > 0


def test_recommendation_generation():
    """Test recommendation generation."""
    engine = RecommendationEngine()
    
    learner_data = {
        "learner_id": 1,
        "education_level": "graduate",
        "prior_skills": ["Python", "Data Analysis"],
        "career_aspirations": ["Data Scientist"],
        "interests": ["Machine Learning"]
    }
    
    recommendations = engine.recommend(learner_data, top_k=5)
    
    assert "recommendations" in recommendations
    assert "model_version" in recommendations
    assert isinstance(recommendations["recommendations"], list)


def test_learning_path_generation():
    """Test learning path generation."""
    engine = RecommendationEngine()
    
    learner_data = {
        "learner_id": 1,
        "education_level": "graduate",
        "prior_skills": ["Python"]
    }
    
    path = engine.generate_learning_path(
        learner_data,
        career_goal="Data Scientist",
        target_nsqf_level="7"
    )
    
    assert "path_nodes" in path
    assert "total_duration_weeks" in path
    assert "target_nsqf_level" in path
    assert isinstance(path["path_nodes"], list)


def test_learner_profile_model():
    """Test learner profile model."""
    model = LearnerProfileModel()
    assert model is not None
    assert model.education_encoder is not None


def test_synthetic_data_generation():
    """Test synthetic training data generation."""
    data = generate_synthetic_training_data(n_samples=100)
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 100
    assert "learner_id" in data.columns
    assert "education_level" in data.columns
    assert "prior_skills" in data.columns
    assert "success_score" in data.columns


def test_model_training():
    """Test model training process."""
    training_data = generate_synthetic_training_data(n_samples=100)
    model = LearnerProfileModel()
    
    metrics = model.train(training_data)
    
    assert "train_score" in metrics
    assert "test_score" in metrics
    assert 0 <= metrics["train_score"] <= 1
    assert 0 <= metrics["test_score"] <= 1


def test_normalize_skills():
    """Test skill normalization."""
    engine = RecommendationEngine()
    
    skills = ["Python", "JavaScript", "Data Analysis"]
    normalized = engine.normalize_skills(skills)
    
    assert isinstance(normalized, list)
    assert len(normalized) == len(skills)


def test_recommendation_with_explanations():
    """Test recommendations include explanations."""
    engine = RecommendationEngine()
    
    learner_data = {
        "learner_id": 1,
        "education_level": "graduate",
        "prior_skills": ["Python"],
        "career_aspirations": ["Software Engineer"],
        "interests": ["Technology"]
    }
    
    recommendations = engine.recommend(
        learner_data,
        top_k=3,
        include_explanations=True
    )
    
    assert "recommendations" in recommendations
    if len(recommendations["recommendations"]) > 0:
        first_rec = recommendations["recommendations"][0]
        assert "explanation" in first_rec or first_rec.get("explanation") is None


def test_recommendation_without_explanations():
    """Test recommendations without explanations."""
    engine = RecommendationEngine()
    
    learner_data = {
        "learner_id": 1,
        "education_level": "graduate",
        "prior_skills": ["Python"],
        "career_aspirations": ["Data Scientist"],
        "interests": ["AI"]
    }
    
    recommendations = engine.recommend(
        learner_data,
        top_k=3,
        include_explanations=False
    )
    
    assert "recommendations" in recommendations
    for rec in recommendations["recommendations"]:
        assert "explanation" not in rec or rec["explanation"] is None
