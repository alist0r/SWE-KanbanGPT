# routes/task.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import SessionLocal
from classes.classes import TaskCreate
from models.models import Task, AITaskDirection
from utils import validators, gpt
import traceback

# Import the JWT-based authentication dependency
from utils.auth import get_current_user
from models.models import User

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''
The create_task api call takes in a ColumnID, CreatedBy, title, and description.
Checks that title and description are valid entries.
Calls the generate_guidance_for_task from gpt.py to create a list of suggestions
to complete the task.
pushes the task title, description, columnid and userid that created it to the database
also stores the response from the AI to the database.
returns the ai response, taskID and the aiResponse
'''
@router.post("/tasks/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    # This dependency will check for a valid JWT and return the current user.
    #current_user: User = Depends(get_current_user)
    ):
    current_user = User(UserID=1)
    if not validators.validate_user_exists(db, current_user.UserID):
        raise HTTPException(status_code=404, detail="User does not exist")

    if not validators.validate_column_exists(db, task.ColumnID):
        raise HTTPException(status_code=404, detail="Column does not exist")

    if not validators.validate_task_title(task.title):
        raise HTTPException(status_code=400, detail="Invalid task title (max 40 characters)")

    if not validators.validate_description(task.description):
        raise HTTPException(status_code=400, detail="Invalid task description")

    try:
        ai_response = gpt.generate_guidance_for_task(task.title, task.description)

        new_task = Task(
            ColumnID=task.ColumnID,
            CreatedBy=current_user.UserID,
            title=task.title,
            description=task.description
        )

        db.add(new_task)
        db.flush()

        ai_entry = AITaskDirection(
            projectID=new_task.column.ProjectID,
            taskID=new_task.TaskID,
            response=ai_response
        )
        db.add(ai_entry)

        db.commit()
        db.refresh(new_task)
        db.refresh(ai_entry)

    except Exception as e:
        db.rollback()
        print("="*80)
        print("EXCEPTION CAUGHT IN /tasks/")
        traceback.print_exc()  # Full traceback
        print("="*80)
        print("Error during task creation:", str(e))
        raise HTTPException(status_code=500, detail="Could not create task or AI guidance")

    return {
        "message": "Task created successfully",
        "taskID": new_task.TaskID,
        "aiResponse": ai_response
    }

'''
@router.post("/tasks/ai")
def create_ai_task(prompt: str, columnID: int, createdBy: int, db: Session = Depends(get_db)):
    from utils import gpt

    # Validate user/column
    if not validators.validate_user_exists(db, createdBy):
        raise HTTPException(status_code=404, detail="User not found")
    if not validators.validate_column_exists(db, columnID):
        raise HTTPException(status_code=404, detail="Column not found")

    task_data = gpt.generate_task_from_prompt(prompt)

    new_task = Task(
        ColumnID=columnID,
        CreatedBy=createdBy,
        title=task_data["title"],
        description=task_data["description"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "AI-generated task created",
        "taskID": new_task.TaskID,
        "title": task_data["title"],
        "description": task_data["description"]
    }
'''