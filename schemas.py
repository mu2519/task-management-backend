from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
