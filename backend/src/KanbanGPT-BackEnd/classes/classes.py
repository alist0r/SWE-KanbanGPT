from pydantic import BaseModel, Field
from datetime import datetime


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

