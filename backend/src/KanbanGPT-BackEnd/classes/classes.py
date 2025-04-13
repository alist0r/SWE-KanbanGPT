from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    name: str

class TaskCreate(BaseModel):
    ColumnID: int
    # CreatedBy is now automatically validated through our authentication
    # CreatedBy: int
    title: str
    description: str

class ProjectCreate(BaseModel):
    title: str
    description: str
    assigned_users: Optional[List[int]] = []  # User IDs

class ProjectResponse(BaseModel):
    message: str
    project_id: int

class AssignmentCreate(BaseModel):
    task_id: int
    assignees: List[int]