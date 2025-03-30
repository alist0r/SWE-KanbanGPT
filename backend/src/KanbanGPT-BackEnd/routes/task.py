# routes/task.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import SessionLocal
from classes.classes import TaskCreate
from models.models import Task
from utils import validators

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if not validators.validate_user_exists(db, task.CreatedBy):
        raise HTTPException(status_code=404, detail="User does not exist")

    if not validators.validate_column_exists(db, task.ColumnID):
        raise HTTPException(status_code=404, detail="Column does not exist")

    if not validators.validate_task_title(task.title):
        raise HTTPException(status_code=400, detail="Invalid task title (max 40 characters)")

    if not validators.validate_description(task.description):
        raise HTTPException(status_code=400, detail="Invalid task description")

    # Create and insert task
    new_task = Task(
        ColumnID=task.ColumnID,
        CreatedBy=task.CreatedBy,
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "taskID": new_task.TaskID}


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
