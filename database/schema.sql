CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    muscle_group TEXT NOT NULL
        CHECK (muscle_group IN ('push', 'pull', 'legs', 'core'))
    chain TEXT NOT NULL
        CHECK (chain IN ('anterior', 'posterior', 'neutral'))
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
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
        CHECK (ended_at >= started_at)
);

CREATE TABLE session_exercises (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES workout_sessions(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    exercise_order INTEGER NOT NULL
        CHECK (exercise_order > 0),
    UNIQUE(session_id, exercise_order)
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    session_exercise_id INTEGER NOT NULL REFERENCES session_exercises(id) ON DELETE CASCADE,
    set_order INTEGER NOT NULL CHECK (set_order > 0),
    weight NUMERIC(4,1) NOT NULL CHECK (weight > 0),
    reps INTEGER NOT NULL
        CHECK (reps > 0),
    rir INTEGER
        CHECK (rir BETWEEN 0 AND 10),
    performed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_exercise_id, set_order)
);

CREATE TABLE exercise_muscle_mapping (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    muscle_id INTEGER NOT NULL REFERENCES muscles(id),
    activation NUMERIC(3,2) NOT NULL 
        CHECK (activation BETWEEN 0.0 AND 1.0),
    UNIQUE (exercise_id, muscle_id)
);