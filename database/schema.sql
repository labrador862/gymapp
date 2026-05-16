CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_of_birth DATE
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    canonical_name TEXT UNIQUE NOT NULL,
    is_compound BOOLEAN NOT NULL,
    fatigue_score NUMERIC(2,1)
        CHECK (fatigue_score BETWEEN 0.0 AND 1.0)
);

CREATE TABLE muscles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE exercise_aliases (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    alias_name TEXT UNIQUE NOT NULL
);

CREATE TABLE bodyweight_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    bodyweight NUMERIC(4,1) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
        CHECK (ended_at >= started_at)
);

CREATE TABLE session_exercises (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES workout_sessions(id),
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    exercise_order INTEGER NOT NULL
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    session_exercise_id INTEGER NOT NULL REFERENCES session_exercises(id),
    set_order INTEGER NOT NULL,
    weight NUMERIC(4,1) NOT NULL CHECK (weight > 0),
    reps INTEGER NOT NULL CHECK (reps > 0),
    rir INTEGER CHECK (rir BETWEEN 0 AND 10),
    UNIQUE(session_exercise_id, set_order)
);