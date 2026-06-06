Some notes on design decisions for the database schema.

--- Users ---

Not directly within the user's table, but I've added cascading deletes to clean up as necessary. If a user is deleted -> all of their workout sessions are deleted -> all exercises in those sessions are deleted -> all sets in those exercises are deleted. 

--- Exercises ---

canonical_name - I knew eventually there would be conflict amongst users over exercise names (e.g., Bench Press, Barbell Bench Press, Flat Bench), so I determined there needed to be one official name for any exercise and all others that referred to the same lift would be dealt with via exercise_aliases and refer to the correct exercise id. 

fatigue_score - Something I plan to play around with, is intended to represent how fatiguing an exercise is (shocker) and will later contribute to a user's "fatigue meter" where I estimate how much fatigue a user is experiencing to help them decide when to take rest days and when to hit certain muscle groups again. While the default meter may have a maximum value of say 10, I plan to introduce a means for the maximum value to fluctuate as users use the app and it learns how their body responds to certain exercises; if the data suggests that you *should* be fatigued by now but are still performing well, clearly you have a greater recovery capacity than expected.

--- Workout Sessions ---

started_at and ended_at - Will later be used for analysis on a user's performance and for suggestions regarding future improvement.

--- Session Exercises ---
exercise_order - Will be very important for analysis and providing guidance, e.g., compound exercises should come earlier in the session as they require the greatest force output and users should be encouraged to restructure their session around that.

--- Sets ---

set_order - Will be very important for evaluating a user's performance; consecutive sets will reveal weaknesses in their ability to recover between sets, endurance, and more.

--- Exercise Muscle Mapping ---

While many exercises are great for isolating muscle groups, others recruit several at once. This can make tracking weekly volume by muscle group difficult. The intention with this table is to define which exercises recruit which muscles, and make an attempt to estimate how much each exercise recruits a given muscle group. For example, barbell bench press is primarily a chest exercise, however the anterior delts and triceps also experience great tension during the lift. An example mapping for this exercise could be [(chest: 1.0), (anterior delts: 0.5), (triceps: 0.5)]. Additionally, this will be extremely useful for automatically classifying each session (e.g., Push, Pull, Back and Biceps).

activation - A value between 0.00 and 1.00 representing an estimate of how much a given muscle group activates during a specific exercise.

