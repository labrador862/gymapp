from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import database

app = FastAPI()

class AddSetRequest(BaseModel):
    reps: int
    weight: float
    rir: int

# get all users
@app.get("/users")
def users():
    users = database.get_all_users()
    return {"users": users}

# start new session
@app.post("/sessions")
def start_session(user_id: int):
    session_id = database.create_workout_session(user_id)
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

@app.post("/sessions/{session_id}/exercises/{session_exercise_id}/sets")
def add_set(session_id: int, session_exercise_id: int, request: AddSetRequest):
    # ensure session exists
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # ensure exercise belongs to this session
    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    # now safe to add set
    set_id = database.add_set(
        session_exercise_id,
        request.reps,
        request.weight,
        request.rir
    )
    
    return {
        "message": "Set added!",
        "set_id": set_id
    }