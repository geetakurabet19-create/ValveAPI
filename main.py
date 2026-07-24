from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = FastAPI()

# MongoDB Connection
mongo_uri = os.getenv("MONGO_URI")
print("Mongo URI:", mongo_uri)

client = MongoClient(mongo_uri)

db = client["ValveDB"]
collection = db["users"]


# Request Model
class User(BaseModel):
    user_id: str
    valve_name: str


# Home API
@app.get("/")
def home():
    return {"message": "Valve API is connected to MongoDB"}


# API 1 - Add User
@app.post("/add-user")
def add_user(user: User):

    collection.insert_one(user.model_dump())

    return {
        "message": "User added successfully"
    }


# API 2 - Get Users
@app.get("/users")
def get_users():

    users = list(collection.find({}, {"_id": 0}))

    return users