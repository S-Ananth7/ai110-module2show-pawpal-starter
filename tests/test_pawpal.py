"""
tests/test_pawpal.py
--------------------
pytest test suite for PawPal+ core behaviours.

Run with:  python -m pytest  (from the project root)
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler, DailyPlan


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

class TestTask:
    def test_mark_complete_changes_status(self):
        """mark_complete() should flip is_complete from False to True."""
        task = Task("Morning walk", 30, priority="high")
        assert task.is_complete is False
        task.mark_complete()
        assert task.is_complete is True

    def test_mark_complete_is_idempotent(self):
        """Calling mark_complete() twice should not raise and status stays True."""
        task = Task("Feeding", 10, priority="medium")
        task.mark_complete()
        task.mark_complete()
        assert task.is_complete is True

    def test_invalid_priority_raises(self):
        """Constructing a Task with an unrecognised priority should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid priority"):
            Task("Bad task", 10, priority="urgent")

    def test_is_high_priority(self):
        """is_high_priority() should return True only for 'high' tasks."""
        assert Task("Walk", 30, priority="high").is_high_priority() is True
        assert Task("Walk", 30, priority="medium").is_high_priority() is False

    def test_to_dict_contains_all_fields(self):
        """to_dict() should include all six expected keys."""
        task = Task("Brush teeth", 5, priority="medium", category="grooming")
        d = task.to_dict()
        assert set(d.keys()) == {
            "title", "duration_minutes", "priority",
            "is_recurring", "category", "is_complete",
        }


# ---------------------------------------------------------------------------
# Pet tests
# ---------------------------------------------------------------------------

class TestPet:
    def test_add_task_increases_task_count(self):
        """Adding a task to a Pet should increase its task list length by 1."""
        pet = Pet(name="Mochi", species="dog")
        assert len(pet.tasks) == 0
        pet.add_task(Task("Walk", 30, priority="high"))
        assert len(pet.tasks) == 1
        pet.add_task(Task("Feed", 10, priority="medium"))
        assert len(pet.tasks) == 2

    def test_remove_task_by_title(self):
        """remove_task() should delete the matching task (case-insensitive)."""
        pet = Pet(name="Luna", species="cat")
        pet.add_task(Task("Feeding", 10, priority="high"))
        pet.add_task(Task("Play", 15, priority="low"))
        pet.remove_task("feeding")          # lower-case should still match
        assert len(pet.tasks) == 1
        assert pet.tasks[0].title == "Play"

    def test_get_tasks_by_priority_order(self):
        """get_tasks_by_priority() should return high → medium → low."""
        pet = Pet(name="Mochi", species="dog")
        pet.add_task(Task("Enrichment", 20, priority="low"))
        pet.add_task(Task("Walk", 30, priority="high"))
        pet.add_task(Task("Brush", 5, priority="medium"))
        sorted_tasks = pet.get_tasks_by_priority()
        assert [t.priority for t in sorted_tasks] == ["high", "medium", "low"]


# ---------------------------------------------------------------------------
# Owner tests
# ---------------------------------------------------------------------------

class TestOwner:
    def test_add_pet_registers_owner_back_reference(self):
        """add_pet() should set pet.owner to this Owner instance."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog")
        owner.add_pet(pet)
        assert pet.owner is owner

    def test_get_all_tasks_aggregates_across_pets(self):
        """get_all_tasks() should return tasks from all pets combined."""
        owner = Owner("Jordan")
        mochi = Pet("Mochi", "dog")
        luna  = Pet("Luna", "cat")
        mochi.add_task(Task("Walk", 30, priority="high"))
        luna.add_task(Task("Feed", 10, priority="medium"))
        owner.add_pet(mochi)
        owner.add_pet(luna)
        assert len(owner.get_all_tasks()) == 2

    def test_get_schedule_window_returns_tuple(self):
        """get_schedule_window() should return (start_time, available_minutes)."""
        owner = Owner("Jordan", available_minutes=60, preferred_start_time="09:00")
        window = owner.get_schedule_window()
        assert window == ("09:00", 60)


# ---------------------------------------------------------------------------
# Scheduler tests
# ---------------------------------------------------------------------------

class TestScheduler:
    def _make_scheduler(self, minutes: int = 90) -> tuple[Scheduler, Pet]:
        owner = Owner("Jordan", available_minutes=minutes)
        pet = Pet("Mochi", "dog")
        owner.add_pet(pet)
        return Scheduler(owner=owner), pet

    def test_build_plan_returns_daily_plan(self):
        """build_plan() should return a DailyPlan instance."""
        scheduler, pet = self._make_scheduler()
        pet.add_task(Task("Walk", 30, priority="high"))
        plan = scheduler.build_plan(pet)
        assert isinstance(plan, DailyPlan)

    def test_completed_tasks_are_skipped(self):
        """Completed tasks should not appear in the generated plan."""
        scheduler, pet = self._make_scheduler()
        done_task = Task("Old walk", 30, priority="high")
        done_task.mark_complete()
        pet.add_task(done_task)
        pet.add_task(Task("Feed", 10, priority="medium"))
        plan = scheduler.build_plan(pet)
        scheduled_titles = [st.task.title for st in plan.scheduled_tasks]
        assert "Old walk" not in scheduled_titles
        assert "Feed" in scheduled_titles

    def test_tasks_exceeding_window_are_excluded(self):
        """A task longer than available_minutes should not be scheduled."""
        scheduler, pet = self._make_scheduler(minutes=15)
        pet.add_task(Task("Long hike", 60, priority="high"))
        pet.add_task(Task("Quick feed", 10, priority="medium"))
        plan = scheduler.build_plan(pet)
        scheduled_titles = [st.task.title for st in plan.scheduled_tasks]
        assert "Long hike" not in scheduled_titles
        assert "Quick feed" in scheduled_titles

    def test_high_priority_scheduled_before_low(self):
        """High-priority tasks must appear before low-priority ones in the plan."""
        scheduler, pet = self._make_scheduler()
        pet.add_task(Task("Play",     20, priority="low"))
        pet.add_task(Task("Walk",     30, priority="high"))
        pet.add_task(Task("Grooming", 10, priority="medium"))
        plan = scheduler.build_plan(pet)
        priorities = [st.task.priority for st in plan.scheduled_tasks]
        # First entry must be high; last must be low
        assert priorities[0] == "high"
        assert priorities[-1] == "low"

    def test_build_all_plans_one_plan_per_pet(self):
        """build_all_plans() should produce exactly one DailyPlan per pet."""
        owner = Owner("Jordan", available_minutes=90)
        for name in ("Mochi", "Luna", "Biscuit"):
            owner.add_pet(Pet(name, "dog"))
        scheduler = Scheduler(owner=owner)
        plans = scheduler.build_all_plans()
        assert len(plans) == 3
