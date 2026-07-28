from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

print("URI Loaded:", "Yes" if uri else "No")

try:
    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )

    print(client.admin.command("ping"))

except Exception as e:
    print(type(e).__name__)
    print(e)