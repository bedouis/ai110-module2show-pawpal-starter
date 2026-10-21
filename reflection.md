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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
