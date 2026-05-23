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

def get_all_users():
    cursor.execute("""
        SELECT id, username, email, date_of_birth
        FROM users;
    """)
    
    users = cursor.fetchall()
    
    return users