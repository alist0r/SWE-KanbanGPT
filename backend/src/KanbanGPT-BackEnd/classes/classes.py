from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=8)
    password: str
    email: str
    name: str

class TaskCreate(BaseModel):
    ColumnID: int
    CreatedBy: int
    title: str
    description: str
