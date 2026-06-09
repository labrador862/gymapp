from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import db.users as users_db

router = APIRouter()

# get all users
@router.get("/users")
def users():
    users = users_db.get_all_users()
    return {"users": users}