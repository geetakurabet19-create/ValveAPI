from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4
import certifi
import os
import traceback
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from fastapi import HTTPException

load_dotenv()

print("MONGO_URI exists:", os.getenv("MONGO_URI") is not None)
print("MONGO_URI starts with:", os.getenv("MONGO_URI")[:25] if os.getenv("MONGO_URI") else "None")


app = FastAPI()

class UserCreate(BaseModel):
    user_role: str = "admin"
    user_name: str
    metadata: Optional[Dict[str, Any]] = {}

client = MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
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
        traceback.print_exc()
        print("ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_users():
    try:
        users = list(users_collection.find({}))

        for user in users:
            user.pop("_id", None)

        return users

    except Exception as e:
        traceback.print_exc()
        print("ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))