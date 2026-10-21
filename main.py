"""Demo of the PawPal+ core classes: build an owner, pets and tasks, then print today's schedule."""

from datetime import date, datetime, time

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


def at(hour: int, minute: int = 0) -> datetime:
    """Return a datetime for the given time today."""
    return datetime.combine(date.today(), time(hour, minute))


def main() -> None:
    # One owner who manages two pets.
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    mia = Pet("Mia", "cat", 5)
    owner.add_pet(rex)
    owner.add_pet(mia)

    # Tasks are added out of time order on purpose, to show the Scheduler sorting them.
    rex.add_task(Task("Evening walk", 30, Priority.MEDIUM, at(18, 0), Frequency.DAILY))
    mia.add_task(Task("Vet check-up", 45, Priority.HIGH, at(9, 30)))
    rex.add_task(Task("Morning walk", 30, Priority.MEDIUM, at(7, 30), Frequency.DAILY))
    mia.add_task(Task("Feed breakfast", 10, Priority.HIGH, at(8, 0), Frequency.DAILY))

    # The Scheduler reads every pet's tasks through the owner.
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan(day=date.today())

    # Column widths: every row uses the same widths so the columns line up.
    time_w, pet_w, task_w, status_w = 5, 8, 16, 7
    header = f"{'Time':<{time_w}}  {'Pet':<{pet_w}}  {'Task':<{task_w}}  {'Status':<{status_w}}"

    print("Today's Schedule")
    print(header)
    print("-" * len(header))
    for pet, task in plan:
        status = "Done" if task.is_complete else "Pending"
        print(
            f"{task.scheduled_time:%H:%M}  {pet.name:<{pet_w}}  "
            f"{task.description:<{task_w}}  {status:<{status_w}}"
        )


if __name__ == "__main__":
    main()
