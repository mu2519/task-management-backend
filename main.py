from typing import Annotated
from hashlib import sha256
from uuid import UUID, uuid4
from fastapi import FastAPI, Depends, Cookie, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def login(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> None:
    username = user.username
    hashed_password = sha256(user.password.encode()).hexdigest()

    db_user = crud.read_user(db=db, username=username)
    if db_user is None:
        crud.create_user(db=db, username=username, hashed_password=hashed_password)
    elif db_user.hashed_password != hashed_password:
        raise HTTPException(status_code=403)

    session_id = uuid4()
    crud.register_session(db=db, session_id=session_id, username=username)

    response = Response()
    response.set_cookie(key="session_id", value=str(session_id))

    return response


@app.get("/users/")
def get_user_tasks(
    session_id: Annotated[UUID, Cookie()],
    db: Session = Depends(get_db),
):
    username = crud.lookup_session(db=db, session_id=session_id)
    if username is None:
        raise HTTPException(status_code=403)
    return crud.read_user_tasks(db=db, username=username)


@app.post("/tasks/")
def create_task(
    task: schemas.TaskCreate,
    session_id: Annotated[UUID, Cookie()],
    db: Session = Depends(get_db)
):
    username = crud.lookup_session(db=db, session_id=session_id)
    if username is None:
        raise HTTPException(status_code=403)
    id = uuid4()
    return crud.create_task(db=db, task=task, id=id, username=username)


@app.get("/tasks/{id}")
def read_task(
    id: UUID,
    session_id: Annotated[UUID, Cookie()],
    db: Session = Depends(get_db)
):
    username = crud.lookup_session(db=db, session_id=session_id)
    if username is None:
        raise HTTPException(status_code=403)
    db_task = crud.read_task(db=db, id=id)
    if db_task is None:
        raise HTTPException(status_code=404)
    if db_task.username != username:
        raise HTTPException(status_code=403)
    return db_task


@app.put("/tasks/{id}")
def update_task(
    id: UUID,
    task: schemas.TaskUpdate,
    session_id: Annotated[UUID, Cookie()],
    db: Session = Depends(get_db),
):
    username = crud.lookup_session(db=db, session_id=session_id)
    if username is None:
        raise HTTPException(status_code=403)
    db_task = crud.read_task(db=db, id=id)
    if db_task is None:
        raise HTTPException(status_code=404)
    if db_task.username != username:
        raise HTTPException(status_code=403)
    crud.update_task(db=db, id=id, task=task)


@app.delete("/tasks/{id}")
def delete_task(
    id: UUID,
    session_id: Annotated[UUID, Cookie()],
    db: Session = Depends(get_db),
):
    username = crud.lookup_session(db=db, session_id=session_id)
    if username is None:
        raise HTTPException(status_code=403)
    db_task = crud.read_task(db=db, id=id)
    if db_task is None:
        raise HTTPException(status_code=404)
    if db_task.username != username:
        raise HTTPException(status_code=403)
    crud.delete_task(db=db, id=id)
