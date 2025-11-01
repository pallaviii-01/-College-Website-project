from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import Course, CourseCreate, NSQFLevel, ProgressUpdate, ProgressRecord
from ..auth import get_current_user, TokenData
from ..utils.db import get_db, CourseDB, ProgressRecordDB, UserDB

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("/", response_model=List[Course])
async def list_courses(
    sector: Optional[str] = Query(None),
    nsqf_level: Optional[NSQFLevel] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all available courses with optional filters."""
    query = db.query(CourseDB).filter(CourseDB.is_active == True)
    
    if sector:
        query = query.filter(CourseDB.sector == sector)
    
    if nsqf_level:
        query = query.filter(CourseDB.nsqf_level == nsqf_level.value)
    
    courses = query.offset(skip).limit(limit).all()
    
    return [
        Course(
            id=course.id,
            title=course.title,
            description=course.description,
            nsqf_level=NSQFLevel(course.nsqf_level),
            sector=course.sector,
            duration_hours=course.duration_hours,
            skills_covered=course.skills_covered,
            prerequisites=course.prerequisites,
            certification_body=course.certification_body,
            is_active=course.is_active,
            created_at=course.created_at
        )
        for course in courses
    ]


@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get details of a specific course."""
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return Course(
        id=course.id,
        title=course.title,
        description=course.description,
        nsqf_level=NSQFLevel(course.nsqf_level),
        sector=course.sector,
        duration_hours=course.duration_hours,
        skills_covered=course.skills_covered,
        prerequisites=course.prerequisites,
        certification_body=course.certification_body,
        is_active=course.is_active,
        created_at=course.created_at
    )


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new course (admin only)."""
    new_course = CourseDB(
        title=course.title,
        description=course.description,
        nsqf_level=course.nsqf_level.value,
        sector=course.sector,
        duration_hours=course.duration_hours,
        skills_covered=course.skills_covered,
        prerequisites=course.prerequisites,
        certification_body=course.certification_body,
        is_active=course.is_active
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return Course(
        id=new_course.id,
        title=new_course.title,
        description=new_course.description,
        nsqf_level=NSQFLevel(new_course.nsqf_level),
        sector=new_course.sector,
        duration_hours=new_course.duration_hours,
        skills_covered=new_course.skills_covered,
        prerequisites=new_course.prerequisites,
        certification_body=new_course.certification_body,
        is_active=new_course.is_active,
        created_at=new_course.created_at
    )


@router.post("/progress", response_model=ProgressRecord, status_code=status.HTTP_201_CREATED)
async def update_progress(
    progress: ProgressUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update learner's progress for a course."""
    user = db.query(UserDB).filter(UserDB.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    course = db.query(CourseDB).filter(CourseDB.id == progress.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    existing_progress = db.query(ProgressRecordDB).filter(
        ProgressRecordDB.learner_id == user.id,
        ProgressRecordDB.course_id == progress.course_id
    ).first()
    
    if existing_progress:
        existing_progress.completion_percentage = progress.completion_percentage
        existing_progress.skills_acquired = progress.skills_acquired
        existing_progress.assessment_score = progress.assessment_score
        db.commit()
        db.refresh(existing_progress)
        db_progress = existing_progress
    else:
        new_progress = ProgressRecordDB(
            learner_id=user.id,
            course_id=progress.course_id,
            completion_percentage=progress.completion_percentage,
            skills_acquired=progress.skills_acquired,
            assessment_score=progress.assessment_score
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        db_progress = new_progress
    
    return ProgressRecord(
        id=db_progress.id,
        learner_id=db_progress.learner_id,
        course_id=db_progress.course_id,
        completion_percentage=db_progress.completion_percentage,
        skills_acquired=db_progress.skills_acquired,
        assessment_score=db_progress.assessment_score,
        updated_at=db_progress.updated_at
    )


@router.get("/progress/my-courses", response_model=List[ProgressRecord])
async def get_my_progress(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all progress records for the current user."""
    user = db.query(UserDB).filter(UserDB.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    progress_records = db.query(ProgressRecordDB).filter(
        ProgressRecordDB.learner_id == user.id
    ).all()
    
    return [
        ProgressRecord(
            id=record.id,
            learner_id=record.learner_id,
            course_id=record.course_id,
            completion_percentage=record.completion_percentage,
            skills_acquired=record.skills_acquired,
            assessment_score=record.assessment_score,
            updated_at=record.updated_at
        )
        for record in progress_records
    ]


@router.get("/sectors", response_model=List[str])
async def list_sectors(db: Session = Depends(get_db)):
    """Get list of all available sectors."""
    sectors = db.query(CourseDB.sector).distinct().all()
    return [sector[0] for sector in sectors if sector[0]]
