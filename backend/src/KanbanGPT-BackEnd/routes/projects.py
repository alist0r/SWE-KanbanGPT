from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.models import Project, ProjectColumn, User
from utils.database import SessionLocal
from utils import validators
from utils.auth import get_current_user


from classes.classes import ProjectCreate, ProjectResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/projects/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_user)

):

    '''comment this next line out after we get user authentication fully functional'''
    current_user = User(UserID=1)
    # Validate assigned users
    for user_id in project.assigned_users:
        if not validators.validate_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"Assigned user {user_id} does not exist")

    # Create project
    new_project = Project(
        Creator=current_user.UserID,
        title=project.title,
        description=project.description
    )

    db.add(new_project)
    db.flush()  

    # Default columns
    default_columns = ["Backlog", "Assigned", "In-Progress", "Ready For Review", "Complete"]
    for col_title in default_columns:
        db.add(ProjectColumn(ProjectID=new_project.ProjectID, title=col_title))

    db.commit()
    db.refresh(new_project)

    return {"message": "Project created successfully", "project_id": new_project.ProjectID}