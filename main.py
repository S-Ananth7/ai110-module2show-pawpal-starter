"""
main.py
-------
PawPal+ demo script — run with:  python main.py

Creates an Owner, two Pets, several Tasks, runs the Scheduler,
and prints a formatted "Today's Schedule" to the terminal.
"""

from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------------------------
# 1. Create the owner
# ---------------------------------------------------------------------------
jordan = Owner(
    name="Jordan",
    available_minutes=90,
    preferred_start_time="08:00",
    preferences=["outdoor walks preferred in the morning"],
)

# ---------------------------------------------------------------------------
# 2. Create pets and register them with the owner
# ---------------------------------------------------------------------------
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)
luna  = Pet(name="Luna",  species="cat", breed="Tabby",     age_years=5)

jordan.add_pet(mochi)
jordan.add_pet(luna)

# ---------------------------------------------------------------------------
# 3. Add tasks (different durations, priorities, and categories)
# ---------------------------------------------------------------------------

# Mochi's tasks
mochi.add_task(Task("Morning walk",       30, priority="high",   category="exercise",    is_recurring=True))
mochi.add_task(Task("Breakfast",          10, priority="high",   category="feeding",     is_recurring=True))
mochi.add_task(Task("Brush teeth",         5, priority="medium", category="grooming"))
mochi.add_task(Task("Enrichment puzzle",  20, priority="low",    category="enrichment"))

# Luna's tasks
luna.add_task(Task("Wet food feeding",    10, priority="high",   category="feeding",     is_recurring=True))
luna.add_task(Task("Litter box clean",     5, priority="medium", category="hygiene",     is_recurring=True))
luna.add_task(Task("Laser pointer play",  15, priority="low",    category="enrichment"))
luna.add_task(Task("Grooming brush",      10, priority="medium", category="grooming"))

# ---------------------------------------------------------------------------
# 4. Run the scheduler and print today's schedule
# ---------------------------------------------------------------------------
scheduler = Scheduler(owner=jordan)

divider = "=" * 56

print()
print(divider)
print("  ** PawPal+ -- Today's Schedule **")
print(f"  Owner: {jordan.name}   |   Budget: {jordan.available_minutes} min")
print(divider)
print()

plans = scheduler.build_all_plans()

for plan in plans:
    print(plan.get_summary())
    print()
    print(plan.explain_plan())
    print()
    print("-" * 56)
    print()

print("All tasks across all pets today:")
all_tasks = jordan.get_all_tasks()
for task in all_tasks:
    status = "[done]" if task.is_complete else "[todo]"
    print(f"  {status}  {task.title} ({task.duration_minutes} min, {task.priority})")

print()
print(divider)
print("  Schedule complete. Have a great day!")
print(divider)
print()
