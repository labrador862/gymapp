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
    exercise_id INTEGER REFERENCES exercises(id),
    alias_name TEXT UNIQUE NOT NULL
);

CREATE TABLE bodyweight_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    user_weight NUMERIC(4,1) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
);