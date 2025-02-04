import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from uuid import UUID, uuid4
import shelve

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

# TODO: make the routers async 


@app.post("/user/{user_id}/profile_picture/")
async def set_profile_picture(user_id: UUID, file: UploadFile = File(...)):
    with shelve.open("users") as users:
        user = users.get(str(user_id))
        if user is None:
            return {"error": "User not found"}

        image_bytes = await file.read()
        user.set_profile_picture(image_bytes)  # Convert to Base64
        users[str(user_id)] = user  # Store back in shelve

    return {"message": "Profile picture updated successfully"}