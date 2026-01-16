Employee Management REST API

A Flask-based REST API for managing employees, built for the HabotConnect Python Backend Developer hiring task.
Supports CRUD operations, token-based authentication, and MongoDB storage.

Features

Token-based authentication

Create, read, update, delete employees

Email uniqueness and name validation

Filter by department/role

Pagination (10 per page)

Proper HTTP status codes

Console logging

Tech Stack

Python 3.10+

Flask, Flask-CORS

MongoDB (PyMongo)

Werkzeug (password hashing)

Project Structure
.
├── app.py           # Main API server
├── login.py         # Authentication & token generation
├── insertdata.py    # Optional: populate sample employees
└── README.md

API Endpoints

Authentication

POST /api/auth/login → Get token

Employees (Authenticated)

POST /api/employees/ → Create

GET /api/employees/ → List (supports filters & pagination)

GET /api/employees/{id} → Get by ID

PUT /api/employees/{id} → Update

DELETE /api/employees/{id} → Delete

How to Run

Clone repo & install dependencies:

git clone https://github.com/your-username/employee-management-api.git
cd employee-management-api
pip install flask flask-cors pymongo werkzeug


Start server:

python app.py


Access API at:

http://localhost:5000

Testing / Demo Workflow

Login via login.py or /api/auth/login to get token.

Add token to Authorization header:

Authorization: Bearer <TOKEN>


Test employee endpoints (CRUD operations).

Optionally, run insertdata.py to populate sample employees.

Example: Create Employee

curl -X POST http://localhost:5000/api/employees/ \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "email": "john@example.com", "department": "IT", "role": "Developer"}'

Notes

All endpoints require token-based authentication

Proper validation and error handling are implemented

Author

Karishma Sandupatla
Python Backend Developer Candidate
GitHub: https://github.com/karishmasandupatla/employee-management-api

Git Upload Commands
git init
git add .
git commit -m "Initial commit: Employee Management REST API"
git branch -M main
git remote add origin https://github.com/your-username/employee-management-api.git
git push -u origin main
