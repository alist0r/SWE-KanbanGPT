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

class TaskMoveRequest(BaseModel):
    task_id: int
    new_column_id: int


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

class ProjectSummary(BaseModel):
    project_id: int
    title: str

class UserInfo(BaseModel):
    user_id: int
    username: str

class LoginRequest(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str

class TaskAIResponse(BaseModel):
    title: str
    description: str
    ai_response: str

class AddUsersToProjectRequest(BaseModel):
    project_id: Optional[int] = None
    project_title: Optional[str] = None
    user_ids: List[int]

    @classmethod
    def validate(cls, values):
        if not values.get("project_id") and not values.get("project_title"):
            raise ValueError("Either project_id or project_title must be provided.")
        return values