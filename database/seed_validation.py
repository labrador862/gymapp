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

def assert_true(condition, message):
    if not condition:
        raise Exception(message)

# -------------------------
# Exercises exist
# -------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM exercises;
""")

exercise_count = cursor.fetchone()[0]

assert_true(
    exercise_count > 0,
    "No exercises seeded."
)

# -------------------------
# Muscles exist
# -------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM muscles;
""")

muscle_count = cursor.fetchone()[0]

assert_true(
    muscle_count > 0,
    "No muscles seeded."
)

# -------------------------
# Every exercise has mappings
# -------------------------

cursor.execute("""
    SELECT e.canonical_name
    FROM exercises e
    LEFT JOIN exercise_muscle_mapping emm
        ON e.id = emm.exercise_id
    WHERE emm.id IS NULL;
""")

unmapped = cursor.fetchall()

assert_true(
    len(unmapped) == 0,
    f"Exercises without mappings: {unmapped}"
)

# -------------------------
# Activation ranges valid
# -------------------------

cursor.execute("""
    SELECT exercise_id, muscle_id, activation
    FROM exercise_muscle_mapping
    WHERE activation < 0
       OR activation > 1;
""")

bad_activations = cursor.fetchall()

assert_true(
    len(bad_activations) == 0,
    f"Invalid activation values: {bad_activations}"
)

# -------------------------
# No duplicate mappings
# -------------------------

cursor.execute("""
    SELECT exercise_id, muscle_id, COUNT(*)
    FROM exercise_muscle_mapping
    GROUP BY exercise_id, muscle_id
    HAVING COUNT(*) > 1;
""")

duplicates = cursor.fetchall()

assert_true(
    len(duplicates) == 0,
    f"Duplicate mappings found: {duplicates}"
)

# -------------------------
# Fatigue score sanity
# -------------------------

cursor.execute("""
    SELECT canonical_name, fatigue_score
    FROM exercises
    WHERE fatigue_score < 0
       OR fatigue_score > 10;
""")

bad_fatigue = cursor.fetchall()

assert_true(
    len(bad_fatigue) == 0,
    f"Invalid fatigue scores: {bad_fatigue}"
)

print("Seed validation passed.")