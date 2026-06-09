from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import db.sessions as sessions_db

router = APIRouter()

class UpdateSessionExerciseRequest(BaseModel):
    exercise_id: int

class AddExerciseRequest(BaseModel):
    exercise_id: int
    
class ExerciseReorderRequest(BaseModel):
    new_pos: int
    
# get full session details
@router.get("/sessions/{session_id}/details")
def get_full_session(session_id: int):
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    details = sessions_db.get_full_session(session_id)

    return {"session_details": details}

# get list of session exercises
@router.get("/sessions/{session_id}/exercises")
def get_session_exercises(session_id: int):
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    exercises = sessions_db.get_session_exercises(session_id)

    return {"exercises": exercises}


# start new session
@router.post("/sessions")
def start_session(user_id: int):
    session_id = sessions_db.create_workout_session(user_id)
    return {
        "message": "Workout session created!",
        "session_id": session_id
    }
    
# end current session
@router.patch("/sessions/{session_id}/end")
def end_workout_session(session_id: int):
    ended_session = sessions_db.end_workout_session(session_id)
    if ended_session is None:
        raise HTTPException(status_code=404, detail="Session not found or already ended")
    return {
        "message": "Workout session successfully ended.",
        "ended_session": ended_session
    }
    
# get any one specific session data (session id, user id, started_at)
@router.get("/sessions/{session_id}")
def get_session(session_id: int): 
    session_data = sessions_db.get_session(session_id)
    if session_data is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session": session_data}

# get active session data
@router.get("/users/{user_id}/active-session")
def get_active_session(user_id: int):
    active_session = sessions_db.get_active_session(user_id)
    if active_session is None:
        raise HTTPException(status_code=404, detail="User does not have active session")
    return {"active_session": active_session}

# get a list of a user's session history
@router.get("/users/{user_id}/sessions")
def get_user_sessions(user_id: int):
    history = sessions_db.get_user_sessions(user_id)
    return {"history": history}

# add exercise to a session
@router.post("/sessions/{session_id}/exercises")
def add_exercise(session_id: int, request: AddExerciseRequest):
    # ensure session exists
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_exercise_id = sessions_db.add_exercise_to_session(
        session_id, 
        request.exercise_id
    )
    
    return {
        "message": "Exercise added to session!",
        "session_exercise_id": session_exercise_id
    }

# change order of exercises performed
@router.patch("/sessions/{session_id}/exercises/{session_exercise_id}/position")
def reorder_exercise(session_id: int, session_exercise_id: int, request: ExerciseReorderRequest):
    updated = sessions_db.reorder_exercises(session_id, session_exercise_id, request.new_pos)
    if updated is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    return {
        "message": "Exercise reordered successfully.",
        "updated_exercise": updated
    }


# change exercise performed
@router.patch("/sessions/{session_id}/exercises/{session_exercise_id}")
def update_session_exercise(session_id: int, session_exercise_id: int, request: UpdateSessionExerciseRequest):
    # confirm session exists
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # confirm this exercise belongs to this session
    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    updated = sessions_db.update_session_exercise(session_exercise_id, request.exercise_id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return {
        "message": "Exercise updated!",
        "updated_exercise": updated
    }
    

# remove an exercise (and all its sets) from a session
@router.delete("/sessions/{session_id}/exercises/{session_exercise_id}")
def delete_session_exercise(session_id: int, session_exercise_id: int):
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    deleted = sessions_db.delete_session_exercise(session_exercise_id)
    return {
        "message": "Exercise removed from session.", 
        "deleted_exercise": deleted
    }
    
# get session label
@router.get("/sessions/{session_id}/label")
def get_session_label(session_id: int):
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions_db.get_session_label(session_id)

    
    
