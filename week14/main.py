# This file acts as a front desk, an Entry Point of the app.
from fastapi import FastAPI
from routes import users    # imports from folder 'routes' the file 'users.py' 

# 'Main Receptionist'
app = FastAPI(
    title="User Management API",
    description="FastAPI backend for managing users",
    version="1.0.0"
)

# the connection between 'Main Receptionist' - 'Department Manager'
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def health_check():
    return {
        "status": "healthy", 
        "message": "API is running"
    }