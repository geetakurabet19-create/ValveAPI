from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4
import certifi
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from fastapi import HTTPException

load_dotenv()

app = FastAPI()

class UserCreate(BaseModel):
    user_role: str = "admin"
    user_name: str
    metadata: Optional[Dict[str, Any]] = {}

client = MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where()
)

db = client["ValveDB"]

users_collection = db["users"]


@app.get("/")
def home():
    return {"message": "Valve API is connected to MongoDB"}


@app.post("/create-user")
def create_user(user: UserCreate):
    print(user.user_name)
    try:
        user_id = str(uuid4())
        new_user = {
            "user_id": user_id,
            "user_role": user.user_role,
            "user_name": user.user_name,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "metadata": user.metadata
        }

        users_collection.insert_one(new_user)

        return {
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_active_users():
    try:
        users = list(users_collection.find({"active": True}))

        for user in users:
            user.pop("_id", None)

        return users

    except Exception as e:
        return {"error": str(e)}