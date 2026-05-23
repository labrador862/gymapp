import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# USERS
def get_all_users():
    cursor.execute("""
        SELECT id, username, email, date_of_birth
        FROM users;
    """)
    
    users = cursor.fetchall()
    
    return users


# SESSIONS
def create_workout_session(user_id):
    cursor.execute("""
        INSERT INTO workout_sessions (user_id)
        VALUES (%s)
        RETURNING id;
    """, (user_id,))
    
    session_id = cursor.fetchone()[0]
    
    conn.commit()
    
    return session_id

def add_exercise_to_session(session_id, exercise_id, exercise_order):
    cursor.execute("""
        INSERT INTO session_exercises (session_id, exercise_id, exercise_order)
        VALUES (%s, %s, %s)
        RETURNING id;
        """, (
            session_id,
            exercise_id,
            exercise_order
        )
    )
    
    session_exercise_id = cursor.fetchone()[0]
    
    conn.commit()
    
    return session_exercise_id

# SETS
def add_set(session_exercise_id, reps, weight, rir):
    
    cursor.execute("""
        SELECT MAX(set_order)
        FROM sets
        WHERE session_exercise_id = %s;
    """, (session_exercise_id))
    current_max = cursor.fetchone()[0]
    
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
    
    set_id = cursor.fetchone()[0]
    
    conn.commit()
    
    return set_id