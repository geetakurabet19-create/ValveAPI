from pymongo import MongoClient
import certifi

connection_string = "mongodb+srv://geetakurabet19_db_user:T6q9DkIMvNlrEYkC@cluster0.uoqu5qk.mongodb.net/?appName=Cluster0"

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)

# Test connection
print(client.server_info())

db = client["ValveDB"]

users_collection = db["users"]

users = users_collection.find()

for user in users:
    print(user)