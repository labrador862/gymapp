import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor(cursor_factory=RealDictCursor)

# USERS

# who uses my app?
def get_all_users():
    cursor.execute("""
        SELECT id, username, email, date_of_birth
        FROM users;
    """)
    
    users = cursor.fetchall()
    
    return users


# SESSIONS

# instantiate a workout session
def create_workout_session(user_id):
    cursor.execute("""
        INSERT INTO workout_sessions (user_id)
        VALUES (%s)
        RETURNING id;
    """, (user_id,))
    
    session_id = cursor.fetchone()["id"]
    
    conn.commit()
    
    return session_id

# end a currently active session
def end_workout_session(session_id):
    cursor.execute("""
        UPDATE workout_sessions
        SET is_active = FALSE
        WHERE id = %s
            AND is_active = TRUE
        RETURNING id;
    """, (session_id,))
    
    ended_session = cursor.fetchone()
    
    conn.commit()
    
    return ended_session

# identify current session
def get_active_session(user_id):
    cursor.execute("""
        SELECT id
        FROM workout_sessions
        WHERE user_id = %s
            AND is_active = TRUE;
    """, (user_id,))
    
    active_session = cursor.fetchone()
    
    return active_session

# display information for a specific session
def get_session(session_id):
    cursor.execute("""
        SELECT id, user_id, started_at
        FROM workout_sessions
        WHERE id = %s;
    """, (session_id,))
    
    session = cursor.fetchone()
    
    return session

# how did i perform in today's session?
def get_full_session(session_id):
    cursor.execute("""
        SELECT ws.id, e.canonical_name, s.set_order, s.weight, s.reps, s.rir, ws.started_at, ws.ended_at
        FROM workout_sessions ws
        JOIN session_exercises se
            ON ws.id = se.session_id
        JOIN exercises e
            ON se.exercise_id = e.id
        JOIN sets s
            ON se.id = s.session_exercise_id
        WHERE ws.id = %s
        ORDER BY se.exercise_order, s.set_order;
    """, (session_id,))
    
    session_details = cursor.fetchall()
    
    return session_details

# how can i see previous sessions?
def get_user_sessions(user_id):
    cursor.execute("""
        SELECT id, started_at, ended_at, 
            ended_at - started_at AS duration
        FROM workout_sessions
        WHERE user_id = %s
        ORDER BY started_at DESC;
    """, (user_id,))
    
    sessions = cursor.fetchall()
    
    return sessions

# add an exercise to my current session
def add_exercise_to_session(session_id, exercise_id):
    cursor.execute("""
        SELECT MAX(exercise_order) AS max_order
        FROM session_exercises
        WHERE session_id = %s;
    """, (session_id,))
    current_max = cursor.fetchone()["max_order"]

    # edge case: first exercise performed
    if current_max is None:
        next_order = 1
    else:
        next_order = current_max + 1

    cursor.execute("""
        INSERT INTO session_exercises (
            session_id,
            exercise_id,
            exercise_order
        )
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (session_id, exercise_id, next_order))

    session_exercise_id = cursor.fetchone()["id"]

    conn.commit()

    return session_exercise_id

# what exercises did i perform during this session?
def get_session_exercises(session_id):
    cursor.execute("""
        SELECT id, exercise_id, exercise_order
        FROM session_exercises
        WHERE session_id = %s
        ORDER BY exercise_order;
    """, (session_id,))
    
    exercises = cursor.fetchall()
    
    return exercises

# is a given exercise in this session?
def get_session_exercise(session_id, session_exercise_id):
    cursor.execute("""
        SELECT id
        FROM session_exercises
        WHERE id = %s
            AND session_id = %s;
    """, (session_exercise_id, session_id))
    
    exercise = cursor.fetchone()

    return exercise

# user selected wrong exercise, allow them to change it
def update_session_exercise(exercise_id, session_exercise_id):
    cursor.execute("""
        UPDATE session_exercises
        SET exercise_id = %s
        WHERE id = %s
        RETURNING id, session_id, exercise_id, exercise_order;
    """, (exercise_id, session_exercise_id))
    
    updated = cursor.fetchone()
    conn.commit()
    
    return updated

# remove an exercise and all its sets from a session
def delete_session_exercise(session_exercise_id):
    cursor.execute("""
        DELETE FROM session_exercises
        WHERE id = %s
        RETURNING id, session_id, exercise_id, exercise_order;
    """, (session_exercise_id,))

    deleted = cursor.fetchone()
    conn.commit()

    return deleted

# change order of exercises
def reorder_exercises(session_id, session_exercise_id, new_pos):
    # get current position of target exercise
    cursor.execute("""
        SELECT exercise_order
        FROM session_exercises
        WHERE id = %s
            AND session_id = %s;
    """, (session_exercise_id, session_id))

    exercise = cursor.fetchone()
    if exercise is None:
        return None
    current_pos = exercise["exercise_order"]
    
    # change nothing if already in desired position
    if current_pos == new_pos:
        return True
    
    # move target exercise out of the way
    # if moving up the list
    if new_pos < current_pos:
        cursor.execute("""
            UPDATE session_exercises
            SET exercise_order = exercise_order + 1
            WHERE session_id = %s
                AND exercise_order >= %s
                AND exercise_order < %s;
        """, (session_id, new_pos, current_pos))
    # if moving down the list
    else:
        cursor.execute("""
            UPDATE session_exercises
            SET exercise_order = exercise_order - 1
            WHERE session_id = %s
                AND exercise_order <= %s
                AND exercise_order > %s;
        """, (session_id, new_pos, current_pos))
    
    # place target into final position
    cursor.execute("""
        UPDATE session_exercises
        SET exercise_order = %s
        WHERE id = %s
        RETURNING id, session_id, exercise_id, exercise_order;
    """, (new_pos, session_exercise_id))

    result = cursor.fetchone()
    conn.commit()

    return result

# SETS

# add a set of this exercise to my session
def add_set(session_exercise_id, reps, weight, rir):
    cursor.execute("""
        SELECT MAX(set_order) AS max_order
        FROM sets
        WHERE session_exercise_id = %s;
    """, (session_exercise_id,))
    current_max = cursor.fetchone()["max_order"]
    
    # edge case: if this is the first set fetchone() will return None
    if current_max is None:
        next_set_order = 1
    else:
        next_set_order = current_max + 1
        
    cursor.execute("""
        INSERT INTO sets (
            session_exercise_id,
            set_order,
            reps,
            weight,
            rir
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (session_exercise_id, next_set_order, reps, weight, rir))
    
    set_id = cursor.fetchone()["id"]
    
    conn.commit()
    
    return set_id

# how did i perform for all sets of this exercise?
def get_sets(session_exercise_id):
    cursor.execute("""
        SELECT id, set_order, weight, reps, rir, performed_at
        FROM sets
        WHERE session_exercise_id = %s
        ORDER BY set_order;
    """, (session_exercise_id,))
    
    sets = cursor.fetchall()
    
    return sets

# is a given set in this session?
def get_set(set_id, session_exercise_id):
    cursor.execute("""
        SELECT id
        FROM sets
        WHERE id = %s
            AND session_exercise_id = %s;
    """, (set_id, session_exercise_id))
    
    set = cursor.fetchone()

    return set

# user entered incorrect data for a set, allow them to change it
def update_set(set_id, reps, weight, rir):
    cursor.execute("""
        UPDATE sets
        SET reps = %s,
            weight = %s,
            rir = %s
        WHERE id = %s
        RETURNING id, set_order, reps, weight, rir, performed_at;
    """, (reps, weight, rir, set_id))
    
    updated = cursor.fetchone()
    conn.commit()
    
    return updated

# remove an entire set from a session exercise
def delete_set(set_id):
    cursor.execute("""
        DELETE FROM sets
        WHERE id = %s
        RETURNING id;
    """, (set_id,))
    
    deleted = cursor.fetchone()
    conn.commit()
    
    return deleted

# EXERCISES

# what is the canonical name for this exercise id?
def get_exercise_name(exercise_id):
    cursor.execute("""
        SELECT canonical_name
        FROM exercises
        WHERE id = %s;        
    """, (exercise_id,))
    
    exercise_name = cursor.fetchone()["canonical_name"]
    
    return exercise_name

#TODO
# what kind of workout did the user perform?
def infer_session_label(session_id):
    # ex: if chest/triceps recruitment makes up 70% or more of session = push day
    return 1