from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    graduated = Column(Boolean)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Lab2",
    description="",
    docs_url="/",
)

class UserCreate(BaseModel):
    name: str
    age: int
    graduated: bool

class UserRead(UserCreate):
    id: UUID

class UserUpdate(BaseModel):
    name: str = None
    age: int = None
    graduated: bool = None

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate):
    user_id = str(uuid4())
    query = User.__table__.insert().values(id=user_id, name=user.name, age=user.age, graduated=user.graduated)
    await database.execute(query)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    query = User.__table__.delete().where(User.id == str(user_id))
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@app.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, user: UserUpdate):
    update_data = user.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")
    query = User.__table__.update().where(User.id == str(user_id)).values(**update_data)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {**update_data, "id": user_id}

@app.patch("/users/{user_id}", response_model=UserRead)
async def update_user_graduated(user_id: UUID, graduated: bool):
    query = User.__table__.update().where(User.id == str(user_id)).values(graduated=graduated)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, "graduated": graduated}

@app.get("/users/", response_model=list[UserRead])
async def get_all_users():
    query = User.__table__.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID):
    query = User.__table__.select().where(User.id == str(user_id))
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user