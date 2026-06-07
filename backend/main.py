from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import database

app = FastAPI()

class AddSetRequest(BaseModel):
    reps: int
    weight: float
    rir: int

class UpdateSetRequest(BaseModel):
    reps: int
    weight: float
    rir: int
    
class AddExerciseRequest(BaseModel):
    exercise_id: int
    
class UpdateSessionExerciseRequest(BaseModel):
    exercise_id: int
    
class ExerciseReorderRequest(BaseModel):
    new_pos: int

# get all users
@app.get("/users")
def users():
    users = database.get_all_users()
    return {"users": users}

# get full session details
@app.get("/sessions/{session_id}/details")
def get_full_session(session_id: int):
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    details = database.get_full_session(session_id)

    return {"session_details": details}

# get list of session exercises
@app.get("/sessions/{session_id}/exercises")
def get_session_exercises(session_id: int):
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    exercises = database.get_session_exercises(session_id)

    return {"exercises": exercises}

# get list of sets for an exercise in a specific session
@app.get("/sessions/{session_id}/exercises/{session_exercise_id}/sets")
def get_sets(session_id: int, session_exercise_id: int):
    # ensure session exists
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # ensure excerise is in this session
    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    sets = database.get_sets(session_exercise_id)

    return {"sets": sets}

# start new session
@app.post("/sessions")
def start_session(user_id: int):
    session_id = database.create_workout_session(user_id)
    return {
        "message": "Workout session created!",
        "session_id": session_id
    }
    
# end current session
@app.patch("/sessions/{session_id}/end")
def end_workout_session(session_id: int):
    ended_session = database.end_workout_session(session_id)
    if ended_session is None:
        raise HTTPException(status_code=404, detail="Session not found or already ended")
    return {
        "message": "Workout session successfully ended.",
        "ended_session": ended_session
    }
    
# get any one specific session data (session id, user id, started_at)
@app.get("/sessions/{session_id}")
def session(session_id: int): 
    session_data = database.get_session(session_id)
    if session_data is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session": session_data}

# get active session data
@app.get("/users/{user_id}/active-session")
def get_active_session(user_id: int):
    active_session = database.get_active_session(user_id)
    if active_session is None:
        raise HTTPException(status_code=404, detail="User does not have active session")
    return {"active_session": active_session}

# get a list of a user's session history
@app.get("/users/{user_id}/sessions")
def get_user_sessions(user_id: int):
    history = database.get_user_sessions(user_id)
    return {"history": history}

# add exercise to a session
@app.post("/sessions/{session_id}/exercises")
def add_exercise(session_id: int, request: AddExerciseRequest):
    # ensure session exists
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_exercise_id = database.add_exercise_to_session(
        session_id, 
        request.exercise_id
    )
    
    return {
        "message": "Exercise added to session!",
        "session_exercise_id": session_exercise_id
    }

# change order of exercises performed
@app.patch("/sessions/{session_id}/exercises/{session_exercise_id}/position")
def reorder_exercise(session_id: int, session_exercise_id: int, request: ExerciseReorderRequest):
    updated = database.reorder_exercises(session_id, session_exercise_id, request.new_pos)
    if updated is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    return {
        "message": "Exercise reordered successfully.",
        "updated_exercise": updated
    }

# add a set to a session
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
    
    # row of new set added
    return {
        "message": "Set added!",
        "set_id": set_id
    }

# change exercise performed
@app.patch("/sessions/{session_id}/exercises/{session_exercise_id}")
def update_session_exercise(session_id: int, session_exercise_id: int, request: UpdateSessionExerciseRequest):
    # confirm session exists
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # confirm this exercise belongs to this session
    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    updated = database.update_session_exercise(session_exercise_id, request.exercise_id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return {
        "message": "Exercise updated!",
        "updated_exercise": updated
    }
    
# edit set data
@app.patch("/sessions/{session_id}/exercises/{session_exercise_id}/sets/{set_id}")
def update_set(session_id: int, session_exercise_id: int, set_id: int, request: UpdateSetRequest):
    # confirm session exists
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # confirm this exercise belongs to this session
    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    # confirm set belongs to this session exercise
    set = database.get_set(set_id, session_exercise_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found for this exercise")
    
    # finally, update set
    updated = database.update_set(set_id, request.reps, request.weight, request.rir)
    if updated is None:
        raise HTTPException(status_code=404, detail="Set not found")
    
    return {
        "message": "Set updated!",
        "updated_set": updated
    }
    
# delete a set
@app.delete("/sessions/{session_id}/exercises/{session_exercise_id}/sets/{set_id}")
def delete_set(session_id: int, session_exercise_id: int, set_id: int):
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    set = database.get_set(set_id, session_exercise_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found for this exercise")

    deleted = database.delete_set(set_id)
    return {
        "message": "Set deleted.", 
        "deleted_set": deleted
    }


# remove an exercise (and all its sets) from a session
@app.delete("/sessions/{session_id}/exercises/{session_exercise_id}")
def delete_session_exercise(session_id: int, session_exercise_id: int):
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session_exercise = database.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    deleted = database.delete_session_exercise(session_exercise_id)
    return {
        "message": "Exercise removed from session.", 
        "deleted_exercise": deleted
    }
    
# get session label
@app.get("/sessions/{session_id}/label")
def get_session_label(session_id: int):
    session = database.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return database.get_session_label(session_id)

    