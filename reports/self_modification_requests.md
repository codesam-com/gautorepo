# Self Modification Requests (Goal Interpreter Upgrade)

The system proposes the following upgrade:

- Replace: agent/goal_interpreter.py
  With: agent/goal_interpreter_V2.py
  Reason: Section-aware parsing to correctly separate goal, deliverables, constraints and test data

## Required manual actions

1. Delete agent/goal_interpreter.py
2. Rename agent/goal_interpreter_V2.py -> agent/goal_interpreter.py

