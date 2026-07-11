# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Sample Output

Run `python main.py` to see the generated daily plan:

```
========================================================
  ** PawPal+ -- Today's Schedule **
  Owner: Jordan   |   Budget: 90 min
========================================================

[PET] Mochi (dog | Shiba Inu)
   Start 08:00  |  65 min total  |  4 task(s)

  [ ]  08:00 - 08:30   Morning walk (30 min) [high]  <- high priority - scheduled first
  [ ]  08:30 - 08:40   Breakfast (10 min) [high]  <- high priority - scheduled first
  [ ]  08:40 - 08:45   Brush teeth (5 min) [medium]  <- fits in remaining 50 min
  [ ]  08:45 - 09:05   Enrichment puzzle (20 min) [low]  <- fits in remaining 45 min

[WHY] Plan for Mochi?
  * Morning walk @ 08:00 -- high priority - scheduled first
  * Breakfast @ 08:30 -- high priority - scheduled first
  * Brush teeth @ 08:40 -- fits in remaining 50 min
  * Enrichment puzzle @ 08:45 -- fits in remaining 45 min

--------------------------------------------------------

[PET] Luna (cat | Tabby)
   Start 08:00  |  40 min total  |  4 task(s)

  [ ]  08:00 - 08:10   Wet food feeding (10 min) [high]  <- high priority - scheduled first
  [ ]  08:10 - 08:15   Litter box clean (5 min) [medium]  <- recurring daily task
  [ ]  08:15 - 08:25   Grooming brush (10 min) [medium]  <- fits in remaining 75 min
  [ ]  08:25 - 08:40   Laser pointer play (15 min) [low]  <- fits in remaining 65 min

[WHY] Plan for Luna?
  * Wet food feeding @ 08:00 -- high priority - scheduled first
  * Litter box clean @ 08:10 -- recurring daily task
  * Grooming brush @ 08:15 -- fits in remaining 75 min
  * Laser pointer play @ 08:25 -- fits in remaining 65 min

========================================================
  Schedule complete. Have a great day!
========================================================
```

## Testing PawPal+

```bash
# Run the full test suite:
python -m pytest tests/ -v

# Run with coverage:
python -m pytest tests/ --cov
```

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1
collected 16 items

tests/test_pawpal.py::TestTask::test_mark_complete_changes_status PASSED
tests/test_pawpal.py::TestTask::test_mark_complete_is_idempotent PASSED
tests/test_pawpal.py::TestTask::test_invalid_priority_raises PASSED
tests/test_pawpal.py::TestTask::test_is_high_priority PASSED
tests/test_pawpal.py::TestTask::test_to_dict_contains_all_fields PASSED
tests/test_pawpal.py::TestPet::test_add_task_increases_task_count PASSED
tests/test_pawpal.py::TestPet::test_remove_task_by_title PASSED
tests/test_pawpal.py::TestPet::test_get_tasks_by_priority_order PASSED
tests/test_pawpal.py::TestOwner::test_add_pet_registers_owner_back_reference PASSED
tests/test_pawpal.py::TestOwner::test_get_all_tasks_aggregates_across_pets PASSED
tests/test_pawpal.py::TestOwner::test_get_schedule_window_returns_tuple PASSED
tests/test_pawpal.py::TestScheduler::test_build_plan_returns_daily_plan PASSED
tests/test_pawpal.py::TestScheduler::test_completed_tasks_are_skipped PASSED
tests/test_pawpal.py::TestScheduler::test_tasks_exceeding_window_are_excluded PASSED
tests/test_pawpal.py::TestScheduler::test_high_priority_scheduled_before_low PASSED
tests/test_pawpal.py::TestScheduler::test_build_all_plans_one_plan_per_pet PASSED

============================= 16 passed in 0.08s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
