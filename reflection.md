# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**


**Core user actions**

The design is built around three things a user should be able to do:

1. **Add a pet.** The owner registers a pet by giving its name, species and age. The pet is added to the owner's list, so one owner can manage several pets.
2. **Schedule a care task for a pet.** The owner picks a pet and adds a task such as a walk, feeding or vet visit. They set a description, a start date and time, how long it takes, a priority, and whether it happens once, daily or weekly. The task is stored under that pet.
3. **See the day's plan and any conflicts.** The owner asks for an ordered view of pending tasks across all their pets, sorted by time or by priority. The app also warns when two tasks overlap in time, naming both pets and tasks. When the owner marks a task complete, it stays in the pet's history. If it repeats, the next occurrence is scheduled automatically.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the class skeleton in `pawpal_system.py`, I made four changes before writing any logic:

1. **Added a `day` parameter to `generate_plan()` and `filter_tasks()`.** My third core action is seeing the day's plan, but the original design had no way to ask for one date. Both methods would have returned every pending task forever. `day` is optional, so leaving it out still returns everything. I updated `diagrams/uml_draft.mmd` to match.
2. **Switched Task, Pet and Owner to `@dataclass(eq=False)`.** The default dataclass equality compares every field, so two identical tasks would count as the same one. That could make `remove_task` or the "does this task belong to this pet" check act on the wrong object. It also makes the classes unhashable, so I couldn't use them as dict keys or in sets, for example to group tasks by pet. With `eq=False`, objects are compared by identity and stay hashable.
3. **`Pet.add_task()` now rejects a task that is already in that pet's list.** Otherwise the same Task object could be added twice, and completing it would change both entries. This check only covers one pet. Sharing one Task object between two different pets isn't blocked yet, so that stays the caller's responsibility.
4. **`Scheduler.complete_task()` also checks that the pet belongs to the owner.** The original check only confirmed the task was in the pet's list, so a pet from a different owner would have passed.

None of these changed the four-class structure or the relationships. The changes tighten behavior and add one optional parameter.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI at almost every stage: brainstorming the four-class design, drafting and refining the Mermaid UML, generating the class skeleton and then the implementation, reviewing my own code, and writing the demo script, the first tests, the docstrings and parts of the README. The most helpful prompts were tightly constrained ones, such as "keep exactly four classes", "do not write implementation code yet" and "do not modify other files". They kept each step small enough for me to check.

The prompt that paid off most was asking for a review of the class skeleton for missing relationships and logic bottlenecks before any logic existed. That review produced the four changes in section 1b: the optional `day` filter, `@dataclass(eq=False)`, the duplicate-task guard and the owner check in `complete_task()`. I approved all four. It also raised other issues, such as duration validation and mixing naive and timezone-aware datetimes, that I haven't acted on yet.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not accept the first UML draft as it was written. It said one-time tasks return nothing, yet it declared `mark_complete()` as returning a plain `Task`, so I had it changed to `Task | None`. Its first `detect_conflicts()` returned only pairs of tasks, which would lose which pet each task belongs to, so I asked for two `(Pet, Task)` pairs instead. I also made the call on where completion lives. AI pointed out that this logic could go on `Pet.complete_task`, and I chose `Scheduler.complete_task(pet, task)`, because the Scheduler is the only class that sees both a pet and a task.

For verification, I ran `python main.py` and checked that tasks from both pets came out in chronological order. I also asked for reviews of `main.py` and of the tests against the assignment requirements before accepting them. During the session, AI ran a throwaway check of recurrence, the error cases and the conflict boundary, and ran `pytest` on my two tests. When plain `pytest` failed with `ModuleNotFoundError`, we found it was an import-path problem and added a `pytest.ini`, after which both ways of running the tests passed. I haven't tested the Scheduler's sorting, filtering or conflict detection with saved tests yet, so I can't claim those are verified.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
