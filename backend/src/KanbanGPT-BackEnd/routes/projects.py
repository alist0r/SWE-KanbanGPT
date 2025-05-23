from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from models.models import Project, ProjectColumn, User, ProjectHasUsers, Task
from classes.classes import UserInfo, AddUsersToProjectRequest
from utils.database import SessionLocal
from utils import validators
from utils.auth import get_current_user
from typing import Optional


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
    current_user: User = Depends(get_current_user), # uncomment this in final release
    db: Session = Depends(get_db)
    ):

    '''comment this next line out after we get user authentication fully functional'''
    # current_user = User(UserID=1)

    # Validate assigned users
    for user_id in project.assigned_users:
        if not validators.validate_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"Assigned user {user_id} does not exist")

    if not validators.validate_title(project.title):
        raise HTTPException(status_code=400, detail="Invalid task title (max 40 characters)")

    if not validators.validate_description(project.description):
        raise HTTPException(status_code=400, detail="Invalid task description")

    try:
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

        assigned_user_ids = set(project.assigned_users)
        assigned_user_ids.add(current_user.UserID)

        for user_id in assigned_user_ids:
            db.add(ProjectHasUsers(ProjectID=new_project.ProjectID, UserID=user_id))

        db.commit()
        db.refresh(new_project)
    except Exception as e:
        db.rollback()
        print("=" * 80)
        print("EXCEPTION CAUGHT IN /projects/")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        raise HTTPException(status_code=500, detail="Could not create project")

    return {"message": "Project created successfully", "project_id": new_project.ProjectID}

'''
This api requests checks to see if a project exists, and if so gathers a list of usernames to return.
Accepts a single projectID
'''
@router.get("/projects/{project_id}/users", response_model=List[UserInfo])
def get_project_users(
        project_id: int,
        # current_user: User = Depends(get_current_user), #commented out for testing purposes to avoid the login-feature being required.
        db: Session = Depends(get_db) ):
    # Check if the project exists first
    project = db.query(Project).filter(Project.ProjectID == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch usernames of users assigned to this project
    users = (
        db.query(User.UserID, User.username)
        .join(ProjectHasUsers, User.UserID == ProjectHasUsers.UserID)
        .filter(ProjectHasUsers.ProjectID == project_id)
        .all()
    )

    if not users:
        raise HTTPException(status_code=404, detail="No users assigned to this project")

    return [UserInfo(user_id=u.UserID, username=u.username) for u in users]



'''
This get_project_tasks queries the database for all tasks related to a projectID. 
Provides the option to only return specific task IDs, or to return all of the taskIDs if the task_id list is empty
'''

@router.get("/projects/{project_id}/tasks")
def get_project_tasks(
    project_id: int,
    task_ids: Optional[List[int]] = Query(default=None),   # accepts a list of task_ids. if empty, all tasks are returned. if provided, then only those tasks are returned
    # current_user: User = Depends(get_current_user),    # remember to uncomment this when we are done testing. this is used for login-authentication.
    db: Session = Depends(get_db)

):
    project = db.query(Project).filter(Project.ProjectID == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    query = db.query(Task).join(ProjectColumn, Task.ColumnID == ProjectColumn.ColumnID).filter(ProjectColumn.ProjectID == project_id)

    if task_ids:
        query = query.filter(Task.TaskID.in_(task_ids))

    tasks = query.all()

    return [
        {
            "project_id": project.ProjectID,
            "project_title": project.title,
            "TaskID": task.TaskID,
            "title": task.title,
            "description": task.description,
            "ColumnID": task.ColumnID,
            "dateCreated": task.dateCreated
        }
        for task in tasks
    ]

'''
This get_project_columns queries the database for all columns related to a projectID.
'''

@router.get("/projects/{project_id}/columns", response_model=List[dict])
def get_project_columns(
    project_id: int,
    # current_user: User = Depends(get_current_user),  # Uncomment in production
    db: Session = Depends(get_db)
):
    # Check if the project exists
    project = db.query(Project).filter(Project.ProjectID == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    columns = db.query(ProjectColumn).filter(ProjectColumn.ProjectID == project_id).all()

    return [{"ColumnID": col.ColumnID, "title": col.title} for col in columns]


# Line Y
@router.post("/projects/add-users")
def add_users_to_project(
    request: AddUsersToProjectRequest,
    #current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_query = db.query(Project)
    if request.project_id:
        project = project_query.filter(Project.ProjectID == request.project_id).first()
    else:
        project = project_query.filter(Project.title == request.project_title).first()


    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    '''
    if not db.query(ProjectHasUsers).filter_by(ProjectID=project.ProjectID, UserID=current_user.UserID).first():
        raise HTTPException(status_code=403, detail="You do not have permission to modify this project")
    '''
    # Add new users
    for user_id in request.user_ids:
        if not validators.validate_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"User ID {user_id} does not exist")
        if db.query(ProjectHasUsers).filter_by(ProjectID=project.ProjectID, UserID=user_id).first():
            continue  # Skip users already added
        db.add(ProjectHasUsers(ProjectID=project.ProjectID, UserID=user_id))

    db.commit()

    return {"message": "Users successfully added to the project"}
