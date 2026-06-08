-- =============================================================
-- seed.sql
-- Static reference data for the muscles table.
-- Run this once after schema.sql to populate lookup tables.
-- =============================================================

-- -------------------------------------------------------------
-- muscles
-- split_category:  push | pull | legs | core
-- chain:           anterior | posterior | neutral
--
-- Rationale:
--   push muscles are anterior (chest, front delts, triceps)
--   pull muscles are posterior (lats, biceps, rear delts, traps)
--   lateral delts and forearms are neutral - neither chain dominant
--   leg classification follows anterior/posterior anatomy
--   abs are core/anterior; spinal erectors are legs/posterior
--   (erectors are seeded under legs because they are the primary
--    posterior chain driver in lower-body compound movements)
-- -------------------------------------------------------------

INSERT INTO muscles (name, split_category, chain) VALUES
    ('Chest',             'push', 'anterior'),
    ('Anterior Delts',    'push', 'anterior'),
    ('Triceps',           'push', 'anterior'),
    ('Lateral Delts',     'push', 'neutral'),
    ('Lats',              'pull', 'posterior'),
    ('Biceps',            'pull', 'posterior'),
    ('Posterior Delts',   'pull', 'posterior'),
    ('Traps',             'pull', 'posterior'),
    ('Forearms',          'pull', 'neutral'),
    ('Spinal Erectors',   'legs', 'posterior'),
    ('Quadriceps',        'legs', 'anterior'),
    ('Hamstrings',        'legs', 'posterior'),
    ('Glutes',            'legs', 'posterior'),
    ('Adductors',         'legs', 'anterior'),
    ('Calves',            'legs', 'neutral'),
    ('Abs',               'core', 'anterior');

-- -------------------------------------------------------------
-- exercises
-- is_compound: TRUE for multi-joint movements, FALSE for isolation
-- fatigue_score: systemic fatigue cost 0.0-1.0
-- -------------------------------------------------------------

INSERT INTO exercises (canonical_name, is_compound, fatigue_score) VALUES
    ('Barbell Bench Press',     TRUE,  0.7),
    ('Lat Pulldown',            TRUE,  0.5),
    ('Dumbbell Curl',           FALSE, 0.2),
    ('Incline Dumbbell Press',  TRUE,  0.6),
    ('Pull Up',                 TRUE,  0.6),
    ('Chest Supported Row',     TRUE,  0.5),
    ('Cable Pullover',          FALSE, 0.3),
    ('Dumbbell Lateral Raise',  FALSE, 0.2),
    ('Reverse Pec Deck',        FALSE, 0.2),
    ('Barbell Deadlift',        TRUE,  1.0),
    ('Barbell Squat',           TRUE,  1.0),
    ('Romanian Deadlift',       TRUE,  0.8),
    ('Leg Press',               TRUE,  0.6),
    ('Leg Extension',           FALSE, 0.2),
    ('Seated Hamstring Curl',   FALSE, 0.2),
    ('Hip Adductor Machine',    FALSE, 0.2),
    ('Back Extension',          FALSE, 0.3),
    ('Barbell Curl',            FALSE, 0.2),
    ('Cable Tricep Pushdown',   FALSE, 0.2),
    ('Machine Chest Fly',       FALSE, 0.3),
    ('Machine Shoulder Press',  TRUE,  0.5),
    ('Wrist Curl',              FALSE, 0.1);

-- =====================================================
-- exercise_muscle_mapping seed
-- Grouped by training split for readability
-- Run after muscles and exercises are seeded
-- =====================================================

-- PUSH ------------------------------------------------

-- Barbell Bench Press
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Bench Press'),
     (SELECT id FROM muscles WHERE name = 'Chest'), 0.90),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Bench Press'),
     (SELECT id FROM muscles WHERE name = 'Triceps'), 0.60),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Bench Press'),
     (SELECT id FROM muscles WHERE name = 'Anterior Delts'), 0.40);

-- Incline Dumbbell Press
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Incline Dumbbell Press'),
     (SELECT id FROM muscles WHERE name = 'Chest'), 0.80),
    ((SELECT id FROM exercises WHERE canonical_name = 'Incline Dumbbell Press'),
     (SELECT id FROM muscles WHERE name = 'Anterior Delts'), 0.70),
    ((SELECT id FROM exercises WHERE canonical_name = 'Incline Dumbbell Press'),
     (SELECT id FROM muscles WHERE name = 'Triceps'), 0.50);

-- Machine Shoulder Press
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Shoulder Press'),
     (SELECT id FROM muscles WHERE name = 'Anterior Delts'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Shoulder Press'),
     (SELECT id FROM muscles WHERE name = 'Triceps'), 0.60),
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Shoulder Press'),
     (SELECT id FROM muscles WHERE name = 'Lateral Delts'), 0.40),
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Shoulder Press'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.20);

-- Cable Tricep Pushdown
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Cable Tricep Pushdown'),
     (SELECT id FROM muscles WHERE name = 'Triceps'), 1.00);

-- Dumbbell Lateral Raise
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Dumbbell Lateral Raise'),
     (SELECT id FROM muscles WHERE name = 'Lateral Delts'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Dumbbell Lateral Raise'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.20);

-- Machine Chest Fly
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Chest Fly'),
     (SELECT id FROM muscles WHERE name = 'Chest'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Machine Chest Fly'),
     (SELECT id FROM muscles WHERE name = 'Anterior Delts'), 0.20);

-- PULL ------------------------------------------------

-- Lat Pulldown
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Lat Pulldown'),
     (SELECT id FROM muscles WHERE name = 'Lats'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Lat Pulldown'),
     (SELECT id FROM muscles WHERE name = 'Biceps'), 0.40),
    ((SELECT id FROM exercises WHERE canonical_name = 'Lat Pulldown'),
     (SELECT id FROM muscles WHERE name = 'Posterior Delts'), 0.20),
    ((SELECT id FROM exercises WHERE canonical_name = 'Lat Pulldown'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.20),
    ((SELECT id FROM exercises WHERE canonical_name = 'Lat Pulldown'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.20);

-- Pull Up
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Pull Up'),
     (SELECT id FROM muscles WHERE name = 'Lats'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Pull Up'),
     (SELECT id FROM muscles WHERE name = 'Biceps'), 0.50),
    ((SELECT id FROM exercises WHERE canonical_name = 'Pull Up'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.30),
    ((SELECT id FROM exercises WHERE canonical_name = 'Pull Up'),
     (SELECT id FROM muscles WHERE name = 'Posterior Delts'), 0.20),
    ((SELECT id FROM exercises WHERE canonical_name = 'Pull Up'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.20);

-- Chest Supported Row
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Chest Supported Row'),
     (SELECT id FROM muscles WHERE name = 'Lats'), 0.70),
    ((SELECT id FROM exercises WHERE canonical_name = 'Chest Supported Row'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.60),
    ((SELECT id FROM exercises WHERE canonical_name = 'Chest Supported Row'),
     (SELECT id FROM muscles WHERE name = 'Posterior Delts'), 0.50),
    ((SELECT id FROM exercises WHERE canonical_name = 'Chest Supported Row'),
     (SELECT id FROM muscles WHERE name = 'Biceps'), 0.40),
    ((SELECT id FROM exercises WHERE canonical_name = 'Chest Supported Row'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.20);

-- Cable Pullover
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Cable Pullover'),
     (SELECT id FROM muscles WHERE name = 'Lats'), 1.00);

-- Reverse Pec Deck
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Reverse Pec Deck'),
     (SELECT id FROM muscles WHERE name = 'Posterior Delts'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Reverse Pec Deck'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.20);

-- Dumbbell Curl
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Dumbbell Curl'),
     (SELECT id FROM muscles WHERE name = 'Biceps'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Dumbbell Curl'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.30);

-- Barbell Curl
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Curl'),
     (SELECT id FROM muscles WHERE name = 'Biceps'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Curl'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.30);

-- LEGS ------------------------------------------------

-- Barbell Deadlift
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Spinal Erectors'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Glutes'), 0.90),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 0.80),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Traps'), 0.60),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Quadriceps'), 0.50),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.40),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Abs'), 0.30);

-- Barbell Squat
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Quadriceps'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Glutes'), 0.80),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Adductors'), 0.50),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Spinal Erectors'), 0.30),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Abs'), 0.30),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 0.20),
    ((SELECT id FROM exercises WHERE canonical_name = 'Barbell Squat'),
     (SELECT id FROM muscles WHERE name = 'Calves'), 0.20);

-- Romanian Deadlift
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Romanian Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Romanian Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Glutes'), 0.80),
    ((SELECT id FROM exercises WHERE canonical_name = 'Romanian Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Spinal Erectors'), 0.70),
    ((SELECT id FROM exercises WHERE canonical_name = 'Romanian Deadlift'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 0.20);

-- Leg Press
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Press'),
     (SELECT id FROM muscles WHERE name = 'Quadriceps'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Press'),
     (SELECT id FROM muscles WHERE name = 'Glutes'), 0.60),
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Press'),
     (SELECT id FROM muscles WHERE name = 'Adductors'), 0.40),
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Press'),
     (SELECT id FROM muscles WHERE name = 'Calves'), 0.20),
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Press'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 0.20);

-- Leg Extension
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Leg Extension'),
     (SELECT id FROM muscles WHERE name = 'Quadriceps'), 1.00);

-- Seated Hamstring Curl
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Seated Hamstring Curl'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 1.00);

-- Hip Adductor Machine
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Hip Adductor Machine'),
     (SELECT id FROM muscles WHERE name = 'Adductors'), 1.00);

-- Back Extension
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Back Extension'),
     (SELECT id FROM muscles WHERE name = 'Spinal Erectors'), 1.00),
    ((SELECT id FROM exercises WHERE canonical_name = 'Back Extension'),
     (SELECT id FROM muscles WHERE name = 'Glutes'), 0.50),
    ((SELECT id FROM exercises WHERE canonical_name = 'Back Extension'),
     (SELECT id FROM muscles WHERE name = 'Hamstrings'), 0.30);

-- OTHER -------------------------------------------------------

-- Wrist Curl
INSERT INTO exercise_muscle_mapping (exercise_id, muscle_id, activation) VALUES
    ((SELECT id FROM exercises WHERE canonical_name = 'Wrist Curl'),
     (SELECT id FROM muscles WHERE name = 'Forearms'), 1.00);