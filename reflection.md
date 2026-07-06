# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML included six classes, each with a single clear responsibility:

- **`Owner`** — stores the pet owner's name, total time available for the day (`available_minutes`), preferred start time, and any care preferences. It acts as the source of scheduling constraints.
- **`Pet`** — a dataclass representing the animal being cared for. It holds a list of `Task` objects and links back to its `Owner`. It is responsible for managing its own task list (add, remove, sort by priority).
- **`Task`** — a dataclass for a single care activity (e.g., "Morning walk"). It holds the title, duration in minutes, priority level, whether it recurs, and a category. It is the core unit of work the scheduler operates on.
- **`Scheduler`** — the planning engine. It takes a `Pet` (which knows its `Owner`) and builds a `DailyPlan` by sorting tasks by priority and greedily fitting them into the available time window.
- **`DailyPlan`** — the output object. It holds an ordered list of `ScheduledTask` entries, tracks total minutes used, and provides human-readable summaries and explanations.
- **`ScheduledTask`** — a wrapper around a `Task` that adds concrete `start_time`, `end_time`, and a `reason` explaining why the task was included. It is created by `DailyPlan.add_entry` during scheduling.

Relationships: `Owner` owns one or more `Pet`s → each `Pet` has zero or more `Task`s → `Scheduler` reads from `Pet` and produces a `DailyPlan` → `DailyPlan` contains `ScheduledTask`s → each `ScheduledTask` wraps a `Task`.

**b. Design changes**

After asking the AI coding assistant to review the skeleton, four improvements were made:

1. **`Task` gained a `__post_init__` priority validator** — the original design had no guard against invalid priority strings (e.g., `"urgent"`). Since `PRIORITY_ORDER` is a fixed dict, passing an unknown key would silently return `None` during sorting. Adding a `ValueError` in `__post_init__` catches this at construction time.

2. **`ScheduledTask` was converted to a `@dataclass`** — the original version used a manual `__init__`. Since it holds only data fields plus one formatting method, converting it to a dataclass makes it consistent with `Task` and `Pet`, reduces boilerplate, and gets `__repr__` for free (useful for debugging).

3. **`Scheduler` now reads `Owner.preferred_start_time`** — the original design hardcoded `"08:00"` in `DailyPlan`. This meant the `Owner` class held a `preferred_start_time` attribute that nothing used. The fix threads that value through `Scheduler.__init__` so the plan's start time actually comes from the owner.

4. **`DailyPlan.add_entry` received a detailed docstring** — the stub gave no hint about how `end_time` should be computed. Without that, the `ScheduledTask` would have no end time and total duration tracking would be broken. The updated docstring makes the implementation contract explicit before any logic is written.


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
