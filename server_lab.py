from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid4
import shelve

# as in the previous lab, use the following command to start your application
# uvicorn server:app --reload

# go through the following link to access swagger
# http://127.0.0.1:8000/


app = FastAPI(
    title="Lab2",
    description="",
    docs_url="/",
    
)

# TODO: define a user pydantic model with required fields

# Define a Pydantic model for the request body
class UserCreate(BaseModel):
    name: str
    age: int
    graduated: bool
    
    
class UserRead(UserCreate): 
    id: UUID

class UserUpdate(UserCreate):
    name: str = None
    age: int = None
    graduated: bool = None
    id: UUID = None

# TODO: implement all the methods below
# TODO: use shelve to have persistently stored dict-like file https://docs.python.org/3/library/shelve.html
## alternatively, use a database of your choice 

@app.post("/users/")
def create_user(user: UserCreate):
    with shelve.open("users_db.csv") as users :
        new_user = UserRead(id = uuid4(), name = user.name, age = user.age, graduated = user.graduated)
        users[str(new_user.id)] = new_user
    return new_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    with shelve.open("users_db.csv") as users : 
        users.pop(str(user_id))

@app.put("/users/{user_id}")
def update_user(user_id: UUID, user: UserUpdate) : 
    with shelve.open("users_db") as users :
        users[str(user_id)] = user

@app.patch("/users/{user_id}")
def update_user_graduated(user_id: UUID, graduated: bool):
    with shelve.open("users_db") as users :
        user = users[str(user_id)]
        user.graduated = graduated
        users[str(user_id)] = user

@app.get("/users/")
def get_all_users(): 
    with shelve.open("users_db") as users :
        return list(users.values())

@app.get("/users/{user_id}")
def get_user(user_id: UUID): 
    with shelve.open("users_db") as users :
        return users[str(user_id)]