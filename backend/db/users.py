from db.connection import conn, cursor

# who uses my app?
def get_all_users():
    cursor.execute("""
        SELECT id, username, email, date_of_birth
        FROM users;
    """)
    
    users = cursor.fetchall()
    
    return users