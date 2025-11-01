import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import json
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/skillpath_db")

def load_courses_from_csv(csv_path: str):
    """Load courses from CSV into database."""
    df = pd.read_csv(csv_path)
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        skills_covered = json.loads(row['skills_covered'].replace("'", '"'))
        prerequisites = json.loads(row['prerequisites'].replace("'", '"'))
        
        cursor.execute("""
            INSERT INTO courses (
                title, description, nsqf_level, sector, duration_hours,
                skills_covered, prerequisites, certification_body, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            row['title'],
            row['description'],
            str(row['nsqf_level']),
            row['sector'],
            row['duration_hours'],
            json.dumps(skills_covered),
            json.dumps(prerequisites),
            row['certification_body'],
            row['is_active']
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Loaded {len(df)} courses into database")


def load_job_market_data(csv_path: str):
    """Load job market data from CSV into database."""
    df = pd.read_csv(csv_path)
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        top_industries = json.loads(row['top_industries'].replace("'", '"'))
        
        cursor.execute("""
            INSERT INTO job_market_data (
                skill_name, demand_score, growth_trend, avg_salary_range, top_industries
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            row['skill_name'],
            row['demand_score'],
            row['growth_trend'],
            row['avg_salary_range'],
            json.dumps(top_industries)
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Loaded {len(df)} job market records into database")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python load_courses.py <courses_csv_path> [job_market_csv_path]")
        sys.exit(1)
    
    courses_path = sys.argv[1]
    load_courses_from_csv(courses_path)
    
    if len(sys.argv) > 2:
        job_market_path = sys.argv[2]
        load_job_market_data(job_market_path)
    
    print("Data loading complete!")
