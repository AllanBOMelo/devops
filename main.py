from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.schema import Base
from services import create_user, get_user, get_users, update_user, delete_user
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

users_db = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/status")
def status():
    return {"status": "running"}


@app.post("/users/", status_code=201)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=422, detail="User already exists")
    users_db[user.id] = user
    return user

@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"detail": "User deleted"}
