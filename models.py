from sqlalchemy import Column, String, Uuid
from .database import Base


class SessionManagement(Base):
    __tablename__ = "sessions"
    session_id = Column(Uuid, primary_key=True)
    username = Column(String)


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    hashed_password = Column(String)


class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Uuid, primary_key=True)
    username = Column(String)
    title = Column(String)
    description = Column(String)
