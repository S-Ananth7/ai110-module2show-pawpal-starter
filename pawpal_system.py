"""
pawpal_system.py
----------------
PawPal+ logic layer — full implementation.

All backend classes live here. Class structure mirrors diagrams/uml.mmd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PRIORITY_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}


def _add_minutes(time_str: str, minutes: int) -> str:
    """Add *minutes* to a 'HH:MM' time string and return the new 'HH:MM' string."""
    t = datetime.strptime(time_str, "%H:%M")
    t += timedelta(minutes=minutes)
    return t.strftime("%H:%M")


# ---------------------------------------------------------------------------
# Task  (dataclass — clean, no boilerplate)
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """A single pet care activity with a title, duration, priority, and completion status."""

    title: str
    duration_minutes: int
    priority: str = "medium"       # "low" | "medium" | "high"
    is_recurring: bool = False
    category: str = "general"      # e.g. "walk", "feeding", "grooming"
    is_complete: bool = False

    def __post_init__(self) -> None:
        """Validate that priority is one of the accepted values."""
        if self.priority not in PRIORITY_ORDER:
            raise ValueError(
                f"Invalid priority '{self.priority}'. "
                f"Must be one of: {list(PRIORITY_ORDER)}"
            )

    def mark_complete(self) -> None:
        """Mark this task as completed so the scheduler will skip it."""
        self.is_complete = True

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"

    def to_dict(self) -> dict:
        """Return a plain-dict representation of every field on this task."""
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "is_recurring": self.is_recurring,
            "category": self.category,
            "is_complete": self.is_complete,
        }


# ---------------------------------------------------------------------------
# Pet  (dataclass — clean, no boilerplate)
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Represents the pet being cared for, including its task list."""

    name: str
    species: str                            # "dog" | "cat" | "other"
    breed: str = "unknown"
    age_years: int = 0
    owner: Optional["Owner"] = field(default=None, repr=False)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append *task* to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the first task whose title matches *title* (case-insensitive)."""
        self.tasks = [t for t in self.tasks if t.title.lower() != title.lower()]

    def get_tasks_by_priority(self) -> list[Task]:
        """Return a new list of tasks sorted high → medium → low."""
        return sorted(self.tasks, key=lambda t: PRIORITY_ORDER[t.priority])


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    """Manages one or more pets and holds the owner's daily scheduling constraints."""

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
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register *pet* under this owner and set its back-reference."""
        pet.owner = self
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets (flat list)."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_schedule_window(self) -> tuple[str, int]:
        """Return (preferred_start_time, available_minutes) for today's plan."""
        return (self.preferred_start_time, self.available_minutes)


# ---------------------------------------------------------------------------
# ScheduledTask  (dataclass — consistent with Task / Pet)
# ---------------------------------------------------------------------------

@dataclass
class ScheduledTask:
    """A Task placed at a specific time slot in the daily plan."""

    task: Task
    start_time: str
    end_time: str
    reason: str = ""

    def format_entry(self) -> str:
        """Return a coloured, human-readable schedule line for this entry."""
        status = "[done]" if self.task.is_complete else "[ ]"
        badge = f"[{self.task.priority}]"
        base = (
            f"  {status}  {self.start_time} - {self.end_time}"
            f"   {self.task.title} ({self.task.duration_minutes} min) {badge}"
        )
        return base + (f"  <- {self.reason}" if self.reason else "")


# ---------------------------------------------------------------------------
# DailyPlan
# ---------------------------------------------------------------------------

class DailyPlan:
    """The generated daily care schedule for a single pet."""

    def __init__(self, pet: Pet, start_time: str = "08:00") -> None:
        self.pet = pet
        self.start_time = start_time
        self.scheduled_tasks: list[ScheduledTask] = []
        self.total_duration_minutes: int = 0

    def add_entry(self, task: Task, start_time: str, reason: str = "") -> None:
        """Compute end_time from start_time + duration, then append a ScheduledTask."""
        end_time = _add_minutes(start_time, task.duration_minutes)
        entry = ScheduledTask(
            task=task,
            start_time=start_time,
            end_time=end_time,
            reason=reason,
        )
        self.scheduled_tasks.append(entry)
        self.total_duration_minutes += task.duration_minutes

    def get_summary(self) -> str:
        """Return a formatted multi-line schedule block for this pet."""
        header = (
            f"[PET] {self.pet.name} ({self.pet.species} | {self.pet.breed})\n"
            f"   Start {self.start_time}  |  "
            f"{self.total_duration_minutes} min total  |  "
            f"{len(self.scheduled_tasks)} task(s)"
        )
        lines = [header, ""]
        for entry in self.scheduled_tasks:
            lines.append(entry.format_entry())
        return "\n".join(lines)

    def explain_plan(self) -> str:
        """Return a narrative explanation of why each task was chosen."""
        lines = [f"[WHY] Plan for {self.pet.name}?"]
        if not self.scheduled_tasks:
            lines.append("  No tasks fit within the available time window.")
            return "\n".join(lines)
        for st in self.scheduled_tasks:
            lines.append(
                f"  * {st.task.title} @ {st.start_time}"
                f" -- {st.reason or 'fits within available window'}"
            )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scheduler  ("Brain" — retrieves, organises, and manages tasks across pets)
# ---------------------------------------------------------------------------

class Scheduler:
    """
    The scheduling brain.

    Receives an Owner, reads all pets' tasks through the owner, sorts them
    by priority, and greedily fits them into the available time window to
    produce one DailyPlan per pet.
    """

    def __init__(self, owner: Owner) -> None:
        """Initialise with an Owner; derive the time window from their settings."""
        self.owner = owner
        self.start_time, self.available_minutes = owner.get_schedule_window()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_plan(self, pet: Pet) -> DailyPlan:
        """Build and return a DailyPlan for *pet* using the owner's time window."""
        plan = DailyPlan(pet=pet, start_time=self.start_time)
        remaining = self.available_minutes
        current_time = self.start_time

        for task in self.sort_by_priority(pet.tasks):
            if task.is_complete:
                continue
            if self.fits_in_window(task, remaining):
                reason = self._reason_for(task, remaining)
                plan.add_entry(task, current_time, reason=reason)
                current_time = _add_minutes(current_time, task.duration_minutes)
                remaining -= task.duration_minutes

        return plan

    def build_all_plans(self) -> list[DailyPlan]:
        """Build a DailyPlan for every pet registered under the owner."""
        return [self.build_plan(pet) for pet in self.owner.pets]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return only incomplete tasks that fit within the full time window."""
        return [
            t for t in tasks
            if not t.is_complete and t.duration_minutes <= self.available_minutes
        ]

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return *tasks* ordered high → medium → low (stable sort)."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority])

    def fits_in_window(self, task: Task, remaining_minutes: int) -> bool:
        """Return True when *task* fits within *remaining_minutes*."""
        return task.duration_minutes <= remaining_minutes

    def _reason_for(self, task: Task, remaining_minutes: int) -> str:
        """Generate a short human-readable reason for including *task*."""
        if task.is_high_priority():
            return "high priority - scheduled first"
        if task.is_recurring:
            return "recurring daily task"
        return f"fits in remaining {remaining_minutes} min"
