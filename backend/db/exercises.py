from db.connection import conn, cursor

# what is the canonical name for this exercise id?
def get_exercise_name(exercise_id):
    cursor.execute("""
        SELECT canonical_name
        FROM exercises
        WHERE id = %s;        
    """, (exercise_id,))
    
    exercise_name = cursor.fetchone()["canonical_name"]
    
    return exercise_name