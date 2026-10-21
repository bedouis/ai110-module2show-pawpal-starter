"""PawPal+ logic layer: Owner, Pet, Task and Scheduler (skeleton only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    duration_minutes: int
    priority: Priority
    scheduled_time: datetime
    frequency: Frequency = Frequency.ONCE
    is_complete: bool = False

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete.

        Returns a new pending Task for DAILY/WEEKLY recurrence (scheduled from
        this task's scheduled_time), or None for ONCE or if already complete.
        """
        pass


@dataclass
class Pet:
    """A pet and the care tasks assigned to it (including completed history)."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        pass

    def get_pending_tasks(self) -> list[Task]:
        """Return the tasks that are not yet complete."""
        pass


@dataclass
class Owner:
    """The person who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def get_all_tasks(self) -> list[PetTask]:
        """Return (pet, task) pairs for every task across all pets."""
        pass


# Type aliases used by the Scheduler.
PetTask = tuple[Pet, Task]
Conflict = tuple[PetTask, PetTask]


class Scheduler:
    """Organizes tasks across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_plan(self) -> list[PetTask]:
        """Return the ordered list of pending (pet, task) pairs to do."""
        pass

    def sort_by_time(self) -> list[PetTask]:
        """Return (pet, task) pairs sorted by scheduled_time."""
        pass

    def sort_by_priority(self) -> list[PetTask]:
        """Return (pet, task) pairs sorted by priority (high first), then scheduled_time."""
        pass

    def filter_tasks(
        self, pet: Optional[Pet] = None, completed: Optional[bool] = None
    ) -> list[PetTask]:
        """Return (pet, task) pairs filtered by pet and/or completion status."""
        pass

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a task for a pet; the application's entry point for completion.

        Raises an error if the task does not belong to the pet. If the task
        recurs, adds the next occurrence to the pet and returns it; otherwise
        returns None.
        """
        pass

    def detect_conflicts(self) -> list[Conflict]:
        """Return each overlapping pair of pending tasks once, with both pets and tasks."""
        pass
