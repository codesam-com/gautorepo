# Self Patch Plan

- improve_goal_verification -> agent/goal_verifier.py (upgrade_candidate)
  - Reason: A stricter verifier exists and should become canonical later
- review_cycle_cohesion -> agent/run_cycle.py (review_candidate)
  - Reason: The canonical cycle should stay aligned with the latest capabilities
