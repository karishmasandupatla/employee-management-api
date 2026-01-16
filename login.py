#Sample Checking Purpose

from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# MongoDB connection
MONGO_URI = "mongodb+srv://karishma_22:mongodb_work7@ks.n6eovrv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["EmployeeDB"]
users = db["users"]

# Create test user
username = "user"
password = "user123"  # choose any password
password_hash = generate_password_hash(password)

# Insert user if not exists
if users.find_one({"username": username}):
    print("User already exists.")
else:
    users.insert_one({
        "username": username,
        "password_hash": password_hash,
        "token": None
    })
    print(f"User '{username}' created with password '{password}'")



