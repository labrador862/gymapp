from db.connection import conn, cursor

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