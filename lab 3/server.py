import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from uuid import UUID, uuid4
import shelve

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
    profile_picture: bytes = None

    def set_profile_picture(self, image_bytes: bytes):
        """Encode bytes as Base64 string"""
        self.profile_picture = base64.b64encode(image_bytes).decode("utf-8")


class UserUpdate(UserCreate):
    profile_picture: bytes = None

    def set_profile_picture(self, image_bytes: bytes):
        """Encode bytes as Base64 string"""
        self.profile_picture = base64.b64encode(image_bytes).decode("utf-8")


# TODO: paste your routers from previous lab in here
@app.post("/users/")
async def create_user(user: UserCreate):
    with shelve.open("users_db") as users :
        new_user = UserRead(id = uuid4(), name = user.name, age = user.age, graduated = user.graduated)
        users[str(new_user.id)] = new_user
    return new_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    with shelve.open("users_db") as users : 
        users.pop(str(user_id))

@app.put("/users/{user_id}")
async def update_user(user_id: UUID, user: UserUpdate) : 
    with shelve.open("users_db") as users :
        users[str(user_id)] = UserRead(id=user_id, profile_picture=user.profile_picture, name=user.name, age=user.age, graduated=user.graduated)

@app.patch("/users/{user_id}")
async def update_user_graduated(user_id: UUID, graduated: bool):
    with shelve.open("users_db") as users :
        user = users[str(user_id)]
        user.graduated = graduated
        users[str(user_id)] = user

@app.get("/users/")
async def get_all_users(): 
    with shelve.open("users_db") as users :
        return list(users.values())

@app.get("/users/{user_id}")
async def get_user(user_id: UUID): 
    with shelve.open("users_db") as users :
        return users[str(user_id)]
# TODO: make the routers async 

@app.post("/users/{user_id}/profile_picture/")
async def set_profile_picture(user_id: UUID, file: UploadFile = File(...)):
    with shelve.open("users_db") as users:
        user = users.get(str(user_id))
        if user is None:
            return {"error": "User not found"}

        image_bytes = await file.read()
        user.set_profile_picture(image_bytes)  # Convert to Base64
        users[str(user_id)] = user  # Store back in shelve

    return {"message": "Profile picture updated successfully"}