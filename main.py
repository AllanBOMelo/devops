from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.schema import Base
from services import create_user, get_user, get_users, update_user, delete_user


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user_endpoint(name: str, email: str, db: Session = Depends(get_db)):
    return create_user(db=db, name=name, email=email)


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        return {"error": str(e)}


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)


@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    try:
        db_user = update_user(db=db, user_id=user_id, name=name, email=email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        return {"error": str(e)}


@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = delete_user(db=db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
