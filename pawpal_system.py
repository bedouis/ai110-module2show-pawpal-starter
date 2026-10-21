"""PawPal+ logic layer: Owner, Pet, Task and Scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, IntEnum
from typing import Optional


class Priority(IntEnum):
    """Task priority. Higher value means more important."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Frequency(Enum):
    """How often a task repeats."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


# Time between occurrences of a recurring task. ONCE tasks do not recur.
_RECURRENCE = {
    Frequency.DAILY: timedelta(days=1),
    Frequency.WEEKLY: timedelta(weeks=1),
}


# eq=False keeps identity-based equality and hashing: two tasks with identical
# fields are still different objects, and Task/Pet/Owner can be used in sets
# and as dict keys.
@dataclass(eq=False)
class Task:
    """A single care activity for a pet."""

    description: str
    duration_minutes: int
    priority: Priority
    scheduled_time: datetime
    frequency: Frequency = Frequency.ONCE
    is_complete: bool = False

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete and return its next occurrence, if any.

        For DAILY/WEEKLY tasks, returns a new pending Task scheduled one day or
        one week after this task's scheduled_time. Returns None for ONCE tasks,
        or if the task was already complete (nothing changes in that case).
        """
        if self.is_complete:
            return None
        self.is_complete = True

        interval = _RECURRENCE.get(self.frequency)
        if interval is None:
            return None
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            scheduled_time=self.scheduled_time + interval,
            frequency=self.frequency,
        )


@dataclass(eq=False)
class Pet:
    """A pet and the care tasks assigned to it (including completed history)."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet. Raises ValueError if this task object is already assigned."""
        if task in self.tasks:
            raise ValueError(f"Task {task.description!r} is already assigned to {self.name}.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet. Raises ValueError if the task is not assigned to it."""
        if task not in self.tasks:
            raise ValueError(f"Task {task.description!r} is not assigned to {self.name}.")
        self.tasks.remove(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return the tasks that are not yet complete."""
        return [task for task in self.tasks if not task.is_complete]


@dataclass(eq=False)
class Owner:
    """The person who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner. Raises ValueError if this pet object is already added."""
        if pet in self.pets:
            raise ValueError(f"{pet.name} is already one of {self.name}'s pets.")
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner. Raises ValueError if the pet is not one of their pets."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not one of {self.name}'s pets.")
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[PetTask]:
        """Return (pet, task) pairs for every task across all pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


# Type aliases used by the Scheduler.
PetTask = tuple[Pet, Task]
Conflict = tuple[PetTask, PetTask]


class Scheduler:
    """Organizes tasks across all of an owner's pets.

    All reads go through Owner.get_all_tasks() and are recomputed on every
    call, so results never go stale when pets or tasks change.
    """

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_plan(self, day: Optional[date] = None) -> list[PetTask]:
        """Return pending (pet, task) pairs sorted by scheduled_time.

        If day is given, only tasks scheduled on that date are included.
        """
        pending = self.filter_tasks(completed=False, day=day)
        return sorted(pending, key=lambda pair: pair[1].scheduled_time)

    def sort_by_time(self) -> list[PetTask]:
        """Return all (pet, task) pairs, completed ones included, sorted by scheduled_time."""
        return sorted(self.owner.get_all_tasks(), key=lambda pair: pair[1].scheduled_time)

    def sort_by_priority(self) -> list[PetTask]:
        """Return all (pet, task) pairs sorted by priority (high first), then by scheduled_time."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda pair: (-pair[1].priority, pair[1].scheduled_time),
        )

    def filter_tasks(
        self,
        pet: Optional[Pet] = None,
        completed: Optional[bool] = None,
        day: Optional[date] = None,
    ) -> list[PetTask]:
        """Return (pet, task) pairs matching every filter given (None means no filter)."""
        return [
            (p, task)
            for p, task in self.owner.get_all_tasks()
            if (pet is None or p is pet)
            and (completed is None or task.is_complete == completed)
            and (day is None or task.scheduled_time.date() == day)
        ]

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a task for a pet and add its next occurrence if it recurs.

        This is the application's entry point for completion. Raises ValueError
        if the pet is not one of the owner's pets or the task is not assigned to
        the pet. Returns the new Task added to the pet, or None if none was created.
        """
        if pet not in self.owner.pets:
            raise ValueError(f"{pet.name} is not one of {self.owner.name}'s pets.")
        if task not in pet.tasks:
            raise ValueError(f"Task {task.description!r} does not belong to {pet.name}.")

        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> list[Conflict]:
        """Return each overlapping pair of pending tasks once, with both pets and tasks.

        A task occupies [scheduled_time, scheduled_time + duration_minutes), so
        back-to-back tasks do not conflict. Pairs are ordered earliest-start first.
        """
        pending = self.filter_tasks(completed=False)
        pending.sort(key=lambda pair: pair[1].scheduled_time)

        conflicts: list[Conflict] = []
        for i, first in enumerate(pending):
            first_end = first[1].scheduled_time + timedelta(minutes=first[1].duration_minutes)
            for second in pending[i + 1:]:
                # Sorted by start, so once a task starts at or after first_end,
                # no later task can overlap first either.
                if second[1].scheduled_time >= first_end:
                    break
                conflicts.append((first, second))
        return conflicts
