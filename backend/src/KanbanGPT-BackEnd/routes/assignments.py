from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.models import Assignment, Task, ProjectColumn, ProjectHasUsers, User
from utils.database import SessionLocal
from utils.auth import get_current_user
from classes.classes import AssignmentCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
Accepts an assignment ID, and a list of userIDs, and updates assignment table to create link between users and tasks

'''
@router.post("/assignments/")
def assign_users_to_task(
    assignment: AssignmentCreate,
    #current_user: User = Depends(get_current_user), # uncomment this in final release
    db: Session = Depends(get_db)
):
    current_user = User(UserID=1)  # Replace with Depends(get_current_user) when ready

    task = db.query(Task).join(ProjectColumn).filter(Task.TaskID == assignment.task_id).first()
    if not task or not task.column:
        raise HTTPException(status_code=404, detail="Task not found or not linked to a project")

    project_id = task.column.ProjectID

    if not db.query(ProjectHasUsers).filter_by(ProjectID=project_id, UserID=current_user.UserID).first():
        raise HTTPException(status_code=403, detail="You are not authorized to assign users to this project")

    successful_assignments = []
    already_assigned = []
    not_in_project = []

    try:
        for user_id in assignment.assignees:
            if not db.query(ProjectHasUsers).filter_by(ProjectID=project_id, UserID=user_id).first():
                not_in_project.append(user_id)
                continue

            if db.query(Assignment).filter_by(TaskID=assignment.task_id, AssigneeID=user_id).first():
                already_assigned.append(user_id)
                continue

            db.add(Assignment(
                TaskID=assignment.task_id,
                AssigneeID=user_id,
                AssignedBy=current_user.UserID
            ))
            successful_assignments.append(user_id)

        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not assign users to task")

    return {
        "message": "Assignment processed with partial success",
        "assigned": successful_assignments,
        "already_assigned": already_assigned,
        "not_in_project": not_in_project
    }

@router.get("/assignments/{task_id}", response_model=List[str])
def get_assignments(
        task_id: int,
        #current_user: User = Depends(get_current_user), # uncomment this in final release
        db: Session = Depends(get_db)
):
    # Ensure the task exists
    task = db.query(Task).filter(Task.TaskID == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Query for users assigned to this task
    assignments = (
        db.query(User.username)
        .join(Assignment, Assignment.AssigneeID == User.UserID)
        .filter(Assignment.TaskID == task_id)
        .all()
    )

    if not assignments:
        raise HTTPException(status_code=404, detail="No users assigned to this task")

    return [user.username for user in assignments]

