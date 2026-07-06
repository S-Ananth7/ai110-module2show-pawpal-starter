"""
pawpal_system.py
----------------
PawPal+ logic layer.

All backend classes live here. Method bodies are stubs — logic will be
added incrementally. Class structure mirrors the UML in diagrams/uml.mmd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    """Represents the pet owner and their scheduling constraints."""

    def __init__(
        self,
        name: str,
        available_minutes: int = 120,
        preferred_start_time: str = "08:00",
        preferences: Optional[list[str]] = None,
    ) -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.preferences: list[str] = preferences or []

    def get_schedule_window(self) -> tuple[str, int]:
        """Return the start time and total minutes available for today.

        Returns:
            A tuple of (preferred_start_time, available_minutes).
        """
        pass  # TODO: implement


# ---------------------------------------------------------------------------
# Task  (dataclass — clean, no boilerplate)
# ---------------------------------------------------------------------------

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet care activity."""

    title: str
    duration_minutes: int
    priority: str = "medium"          # "low" | "medium" | "high"
    is_recurring: bool = False
    category: str = "general"         # e.g. "walk", "feeding", "grooming"

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        pass  # TODO: implement

    def to_dict(self) -> dict:
        """Return a plain-dict representation of this task."""
        pass  # TODO: implement


# ---------------------------------------------------------------------------
# Pet  (dataclass — clean, no boilerplate)
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Represents the pet being cared for."""

    name: str
    species: str                          # "dog" | "cat" | "other"
    breed: str = "unknown"
    age_years: int = 0
    owner: Optional[Owner] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        pass  # TODO: implement

    def remove_task(self, title: str) -> None:
        """Remove a task by title (case-insensitive match)."""
        pass  # TODO: implement

    def get_tasks_by_priority(self) -> list[Task]:
        """Return tasks sorted high → medium → low."""
        pass  # TODO: implement


# ---------------------------------------------------------------------------
# ScheduledTask
# ---------------------------------------------------------------------------

class ScheduledTask:
    """A Task that has been placed at a specific time in the plan."""

    def __init__(
        self,
        task: Task,
        start_time: str,
        end_time: str,
        reason: str = "",
    ) -> None:
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason

    def format_entry(self) -> str:
        """Return a human-readable line for this scheduled task.

        Example:
            '08:00 — Morning walk (20 min) [high] — reason: high priority'
        """
        pass  # TODO: implement


# ---------------------------------------------------------------------------
# DailyPlan
# ---------------------------------------------------------------------------

class DailyPlan:
    """The generated daily care schedule for a pet."""

    def __init__(self, pet: Pet, start_time: str = "08:00") -> None:
        self.pet = pet
        self.start_time = start_time
        self.scheduled_tasks: list[ScheduledTask] = []
        self.total_duration_minutes: int = 0

    def add_entry(self, task: Task, start_time: str) -> None:
        """Wrap a Task in a ScheduledTask and append it to the plan."""
        pass  # TODO: implement

    def get_summary(self) -> str:
        """Return a short multi-line summary of the plan."""
        pass  # TODO: implement

    def explain_plan(self) -> str:
        """Return a narrative explanation of why each task was chosen."""
        pass  # TODO: implement


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """Builds a DailyPlan for a Pet given time constraints."""

    def __init__(self, pet: Pet, available_minutes: Optional[int] = None) -> None:
        self.pet = pet
        # Fall back to owner's window if not explicitly overridden
        self.available_minutes = (
            available_minutes
            if available_minutes is not None
            else (pet.owner.available_minutes if pet.owner else 120)
        )

    def build_plan(self) -> DailyPlan:
        """Sort and fit tasks into available time; return a DailyPlan."""
        pass  # TODO: implement

    def filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Remove tasks that cannot fit in the remaining window."""
        pass  # TODO: implement

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered high → medium → low."""
        pass  # TODO: implement

    def fits_in_window(self, task: Task, remaining_minutes: int) -> bool:
        """Return True if task.duration_minutes <= remaining_minutes."""
        pass  # TODO: implement
