from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash
from functools import wraps
import os
import datetime
import uuid
import re
from bson.objectid import ObjectId
from flask_cors import CORS
import logging


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# App setup
app = Flask(__name__)
CORS(app)


# MongoDB connection
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://karishma_22:mongodb_work7@ks.n6eovrv.mongodb.net/?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    logger.info("MongoDB connected successfully")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")

db = client["EmployeeDB"]
employees = db["employees"]
users = db["users"]

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


# Token authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None

        if not token:
            logger.warning("Token missing")
            return jsonify({"message": "Token is missing"}), 401

        user = users.find_one({"token": token})
        if not user:
            logger.warning("Invalid token")
            return jsonify({"message": "Invalid or expired token"}), 401

        logger.info(f"Authorized user: {user['username']}")
        return f(*args, **kwargs)

    return decorated


# Helper
def get_employee_or_404(emp_id):
    try:
        emp_id = ObjectId(emp_id)
    except Exception:
        return None, jsonify({"message": "Invalid employee ID"}), 400

    employee = employees.find_one({"_id": emp_id})
    if not employee:
        return None, jsonify({"message": "Employee not found"}), 404

    return employee, None


# AUTH LOGIN
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    logger.info("Login request")

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "username and password required"}), 400

    user = users.find_one({"username": data["username"]})
    if not user or not check_password_hash(user["password_hash"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = str(uuid.uuid4())
    users.update_one(
        {"_id": user["_id"]},
        {"$set": {"token": token, "last_login": datetime.datetime.utcnow()}}
    )

    logger.info(f"User logged in: {user['username']}")
    return jsonify({"token": token}), 200


# CREATE EMPLOYEE
@app.route("/api/employees/", methods=["POST"])
@token_required
def create_employee():
    data = request.get_json()
    logger.info("Create employee request")

    if not data or "name" not in data or "email" not in data:
        return jsonify({"message": "name and email required"}), 400

    if not data["name"].strip():
        return jsonify({"message": "Name cannot be empty"}), 400

    email = data["email"].strip().lower()
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"message": "Invalid email format"}), 400

    if employees.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    now = datetime.datetime.utcnow()
    employee = {
        "name": data["name"].strip(),
        "email": email,
        "department": data.get("department"),
        "role": data.get("role"),
        "date_joined": now
    }

    result = employees.insert_one(employee)
    employee["_id"] = str(result.inserted_id)

    logger.info(f"Employee created: {email}")
    return jsonify(employee), 201


# LIST EMPLOYEES (FILTER + PAGINATION)
@app.route("/api/employees/", methods=["GET"])
@token_required
def list_employees():
    logger.info("List employees request")

    query = {}
    if "department" in request.args:
        query["department"] = request.args["department"]
    if "role" in request.args:
        query["role"] = request.args["role"]

    page = int(request.args.get("page", 1))
    limit = 10
    skip = (page - 1) * limit

    cursor = employees.find(query).skip(skip).limit(limit)
    result = []

    for emp in cursor:
        emp["_id"] = str(emp["_id"])
        result.append(emp)

    total = employees.count_documents(query)

    return jsonify({
        "employees": result,
        "page": page,
        "total_pages": (total + limit - 1) // limit,
        "total_records": total
    }), 200


# GET SINGLE EMPLOYEE
@app.route("/api/employees/<emp_id>", methods=["GET"])
@token_required
def get_employee(emp_id):
    employee, error = get_employee_or_404(emp_id)
    if error:
        return error

    employee["_id"] = str(employee["_id"])
    logger.info(f"Fetched employee: {emp_id}")
    return jsonify(employee), 200

# -------------------------------------------------
# UPDATE EMPLOYEE
# -------------------------------------------------
@app.route("/api/employees/<emp_id>", methods=["PUT"])
@token_required
def update_employee(emp_id):
    employee, error = get_employee_or_404(emp_id)
    if error:
        return error

    data = request.get_json()
    update_fields = {}

    if "name" in data:
        if not data["name"].strip():
            return jsonify({"message": "Name cannot be empty"}), 400
        update_fields["name"] = data["name"].strip()

    if "email" in data:
        email = data["email"].strip().lower()
        if not re.match(EMAIL_REGEX, email):
            return jsonify({"message": "Invalid email format"}), 400
        if employees.find_one({"email": email, "_id": {"$ne": ObjectId(emp_id)}}):
            return jsonify({"message": "Email already exists"}), 400
        update_fields["email"] = email

    for field in ["department", "role"]:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return jsonify({"message": "No valid fields to update"}), 400

    employees.update_one(
        {"_id": ObjectId(emp_id)},
        {"$set": update_fields}
    )

    logger.info(f"Employee updated: {emp_id}")
    return jsonify({"message": "Employee updated"}), 200


# DELETE EMPLOYEE
@app.route("/api/employees/<emp_id>", methods=["DELETE"])
@token_required
def delete_employee(emp_id):
    employee, error = get_employee_or_404(emp_id)
    if error:
        return error

    employees.delete_one({"_id": ObjectId(emp_id)})
    logger.info(f"Employee deleted: {emp_id}")

    return "", 204


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)
