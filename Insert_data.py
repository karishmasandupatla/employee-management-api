#Sample Checking Purpose

from pymongo import MongoClient
import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://karishma_22:mongodb_work7@ks.n6eovrv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["EmployeeDB"]
employees = db["employees"]

# Sample employees (5 now)
sample_employees = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "HR",
        "role": "Manager",
        "date_joined": datetime.datetime.utcnow().isoformat(),
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "department": "Engineering",
        "role": "Developer",
        "date_joined": datetime.datetime.utcnow().isoformat(),
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "department": "Sales",
        "role": "Analyst",
        "date_joined": datetime.datetime.utcnow().isoformat(),
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Bob Williams",
        "email": "bob.williams@example.com",
        "department": "Engineering",
        "role": "Developer",
        "date_joined": datetime.datetime.utcnow().isoformat(),
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Clara Brown",
        "email": "clara.brown@example.com",
        "department": "HR",
        "role": "Recruiter",
        "date_joined": datetime.datetime.utcnow().isoformat(),
        "created_at": datetime.datetime.utcnow()
    }
]

# Insert only if not exists
for emp in sample_employees:
    if not employees.find_one({"email": emp["email"]}):
        employees.insert_one(emp)
        print(f"Inserted {emp['name']}")
    else:
        print(f"{emp['name']} already exists")
