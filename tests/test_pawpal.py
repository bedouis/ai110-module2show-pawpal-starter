"""Initial tests for the PawPal+ logic layer."""

from datetime import datetime

from pawpal_system import Frequency, Pet, Priority, Task


def test_task_completion():
    """mark_complete() flips a task's is_complete flag from False to True."""
    # Arrange
    task = Task(
        description="Morning walk",
        duration_minutes=30,
        priority=Priority.MEDIUM,
        scheduled_time=datetime(2026, 10, 20, 8, 0),
        frequency=Frequency.ONCE,
    )
    assert task.is_complete is False  # starting state

    # Act
    task.mark_complete()

    # Assert
    assert task.is_complete is True


def test_task_addition():
    """add_task() adds exactly one task to the pet's task list."""
    # Arrange
    pet = Pet(name="Rex", species="dog", age=3)
    task = Task(
        description="Feed breakfast",
        duration_minutes=10,
        priority=Priority.HIGH,
        scheduled_time=datetime(2026, 10, 20, 7, 30),
        frequency=Frequency.ONCE,
    )
    initial_count = len(pet.tasks)

    # Act
    pet.add_task(task)

    # Assert
    assert len(pet.tasks) == initial_count + 1
    assert task in pet.tasks
