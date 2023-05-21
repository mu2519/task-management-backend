from sqlalchemy import Column, String, Uuid, DateTime
from .database import Base


class SessionManagement(Base):
    __tablename__ = "sessions"
    session_id = Column(Uuid, primary_key=True)
    username = Column(String(100), nullable=False)


class User(Base):
    __tablename__ = "users"
    username = Column(String(100), primary_key=True)
    hashed_password = Column(String(70), nullable=False)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Uuid, primary_key=True)
    username = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    deadline = Column(DateTime, nullable=True)
