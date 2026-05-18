from fastapi import FastAPI
from database import cursor

app = FastAPI()

@app.get("/users")
def get_users():
    cursor.execute("""
        SELECT id, username, email, date_of_birth
        FROM users;
        """)
    users = cursor.fetchall()
    
    return {"users": users}