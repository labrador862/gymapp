from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import db.sets as sets_db
import db.sessions as sessions_db

router = APIRouter()

class AddSetRequest(BaseModel):
    reps: int
    weight: float
    rir: int

class UpdateSetRequest(BaseModel):
    reps: int
    weight: float
    rir: int

# add a set to a session
@router.post("/sessions/{session_id}/exercises/{session_exercise_id}/sets")
def add_set(session_id: int, session_exercise_id: int, request: AddSetRequest):
    # ensure session exists
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # ensure exercise belongs to this session
    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    # now safe to add set
    set_id = sets_db.add_set(
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

# edit set data
@router.patch("/sessions/{session_id}/exercises/{session_exercise_id}/sets/{set_id}")
def update_set(session_id: int, session_exercise_id: int, set_id: int, request: UpdateSetRequest):
    # confirm session exists
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # confirm this exercise belongs to this session
    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")
    
    # confirm set belongs to this session exercise
    set = sets_db.get_set(set_id, session_exercise_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found for this exercise")
    
    # finally, update set
    updated = sets_db.update_set(set_id, request.reps, request.weight, request.rir)
    if updated is None:
        raise HTTPException(status_code=404, detail="Set not found")
    
    return {
        "message": "Set updated!",
        "updated_set": updated
    }
    
# delete a set
@router.delete("/sessions/{session_id}/exercises/{session_exercise_id}/sets/{set_id}")
def delete_set(session_id: int, session_exercise_id: int, set_id: int):
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    set = sets_db.get_set(set_id, session_exercise_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found for this exercise")

    deleted = sets_db.delete_set(set_id)
    return {
        "message": "Set deleted.", 
        "deleted_set": deleted
    }

# get list of sets for an exercise in a specific session
@router.get("/sessions/{session_id}/exercises/{session_exercise_id}/sets")
def get_sets(session_id: int, session_exercise_id: int):
    # ensure session exists
    session = sessions_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # ensure excerise is in this session
    session_exercise = sessions_db.get_session_exercise(session_id, session_exercise_id)
    if session_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found in this session")

    sets = sets_db.get_sets(session_exercise_id)

    return {"sets": sets}