from fastapi import FastAPI
import database

app = FastAPI()

# get all users
@app.get("/users")
def users():
    users = database.get_all_users()
    
    return {
        "users": users
    }
    
# start new session
@app.post("/sessions")
def start_session(user_id: int):
    session_id = database.create_workout_session(user_id)
    
    return {
        "message": "Workout session created!",
        "session_id": session_id
    }