from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import database

app = FastAPI()

# get all users
@app.get("/users")
def users():
    users = database.get_all_users()
    
    return {"users": users}

class StartSessionRequest(BaseModel):
    user_id: int

# start new session
@app.post("/sessions")
def start_session(request: StartSessionRequest):
    session_id = database.create_workout_session(request.user_id)
    
    return {
        "message": "Workout session created!",
        "session_id": session_id
    }
    
# get specific session data
@app.get("/sessions/{session_id}")
def session(session_id: int): 
    session_data = database.get_session(session_id)
    if session_data is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"session": session_data}
    
