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
    ('Pec Deck Chest Fly',      FALSE, 0.3),
    ('Machine Shoulder Press',  TRUE,  0.5),
    ('Wrist Curl',              FALSE, 0.1);