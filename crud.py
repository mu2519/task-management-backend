from uuid import UUID
from sqlalchemy.orm import Session
from . import models, schemas


def register_session(db: Session, session_id: UUID, username: str):
    db_session = models.SessionManagement(session_id=session_id, username=username)
    db.add(db_session)
    db.commit()
    db.expire(db_session)


def lookup_session(db: Session, session_id: UUID):
    db_session = db.query(models.SessionManagement).filter(models.SessionManagement.session_id == session_id).one_or_none()
    if db_session is None:
        return None
    else:
        return db_session.username


def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.expire(db_user)


def read_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def read_user_tasks(db: Session, username: str):
    return db.query(models.Task).filter(models.Task.username == username).all()


def create_task(db: Session, task: schemas.TaskCreate, id: UUID, username: str):
    db_task = models.Task(**task.dict(), id=id, username=username)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def read_task(db: Session, id: UUID):
    return db.query(models.Task).filter(models.Task.id == id).one_or_none()


def update_task(db: Session, id: UUID, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == id).one()
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.deadline is not None:
        db_task.deadline = task.deadline
    db.commit()


def delete_task(db: Session, id: UUID):
    db_task = db.query(models.Task).filter(models.Task.id == id).one()
    db.delete(db_task)
    db.commit()
