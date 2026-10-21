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

## 🖥️ Sample Output

`main.py` is a command-line demo of how the four core classes work together. It creates one `Owner` with two `Pet`s, assigns each pet several `Task`s, and then asks a `Scheduler` for today's plan.

Run it from the project root:

```bash
python main.py
```

Output:

```text
Today's Schedule
Time   Pet       Task              Status
------------------------------------------
07:30  Rex       Morning walk      Pending
08:00  Mia       Feed breakfast    Pending
09:30  Mia       Vet check-up      Pending
18:00  Rex       Evening walk      Pending
```

**What this shows**

- **Multi-pet scheduling:** The `Scheduler` is given only the `Owner`. It gathers tasks from every pet through `Owner.get_all_tasks()`, so Rex's and Mia's tasks appear together in one plan, and each row names the pet it belongs to.
- **Chronological ordering:** The tasks were added in a different order (18:00, 09:30, 07:30, 08:00). `Scheduler.generate_plan()` returns them sorted by scheduled time, so the plan reads from morning to evening regardless of which pet each task belongs to.

## 🧩 Implementation Summary

The logic layer in `pawpal_system.py` has four classes:

- **`Owner`** manages multiple pets. It adds and removes pets, and `get_all_tasks()` returns `(pet, task)` pairs for every task across all of its pets.
- **`Pet`** stores a pet's name, species, age and its list of `Task`s. It adds and removes tasks, rejects duplicates, and reports pending tasks. Completed tasks stay in the list as history.
- **`Task`** represents one care activity: description, duration, `Priority`, scheduled `datetime`, `Frequency` and completion status. `mark_complete()` sets the flag and, for `DAILY` or `WEEKLY` tasks, returns a new pending task one day or one week later.
- **`Scheduler`** is created with an `Owner` and reads every pet's tasks through `Owner.get_all_tasks()`. It sorts by time or priority, filters by pet, completion and date, builds a daily plan, completes tasks (adding the next occurrence of recurring ones), and detects overlapping tasks.

Together, the `Owner` holds the pets, each `Pet` holds its tasks, and the `Scheduler` combines them into a single chronological plan across all pets.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
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
