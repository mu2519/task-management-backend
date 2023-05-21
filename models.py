from sqlalchemy import Column, String, Uuid, DateTime
from .database import Base


class SessionManagement(Base):
    __tablename__ = "sessions"
    session_id = Column(Uuid, primary_key=True)
    username = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Uuid, primary_key=True)
    username = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=True)
