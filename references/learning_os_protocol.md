# AI Learning OS Protocol

Load this reference when the user asks for dynamic learning, review memory, spaced repetition, project-driven learning, exercise generation, code-error analysis, or difficulty adjustment.

## Operating Modes

Classify each turn into one primary mode:

- `onboarding`: discover goals, background, constraints, and target project.
- `concept`: teach one concept with analogy, demo, engineering use, pitfalls, and recall.
- `project`: guide a concrete project step and tie it back to concepts.
- `practice`: generate exercises or evaluate the user's answer.
- `review`: run spaced repetition and memory recall.
- `debug`: analyze code, logs, test failures, or wrong answers.
- `calibration`: adjust difficulty based on observed performance.

## Learning State Schema

Use this shape when persistent memory, the bundled `learning_accelerator` JSON store, or a host-provided state store exists. If no storage exists, include a compact version in the answer under `学习状态` and `状态更新`.

```json
{
  "learner_profile": {
    "known_stack": ["JavaScript", "TypeScript", "React"],
    "preferred_language": "zh-CN",
    "learning_goal": "",
    "target_project": "",
    "constraints": []
  },
  "topic_state": {
    "current_topic": "",
    "level": "beginner|intermediate|advanced",
    "mastered_concepts": [],
    "weak_concepts": [],
    "misconceptions": [],
    "open_questions": []
  },
  "practice_state": {
    "completed_exercises": [],
    "failed_exercises": [],
    "current_project_tasks": [],
    "last_code_errors": []
  },
  "review_state": {
    "due_items": [],
    "review_history": [],
    "next_review_items": []
  },
  "difficulty_state": {
    "current_difficulty": 1,
    "evidence": [],
    "next_adjustment": "easier|same|harder"
  }
}
```

## Spaced Repetition

Use short intervals for new or weak concepts. A simple default is:

- First correct recall: review after 1 day.
- Second correct recall: review after 3 days.
- Third correct recall: review after 7 days.
- Incorrect or fuzzy recall: review again in the current session and keep it in weak concepts.

Do not ask the user to review everything. Select 2-5 high-value items:

- recently learned core concepts,
- repeated mistakes,
- concepts required by the next project step,
- concepts the user could not explain back.

## Exercise Generation

Generate exercises with:

- `goal`: what concept it tests,
- `task`: what to build or answer,
- `input/output`: concrete expected behavior when applicable,
- `constraints`: what must or must not be used,
- `evaluation`: how the answer will be judged,
- `hint`: one optional hint, hidden until needed.

Use three levels:

- `easy`: direct application of the just-learned concept.
- `normal`: combine the concept with one familiar idea.
- `stretch`: apply it in a realistic project-like scenario.

## Code Error Analysis

When the user provides code, logs, or a failing test:

1. Reproduce the likely failure path from the provided evidence.
2. Identify the root cause, not only the surface error.
3. Map the error to the missing concept or misconception.
4. Provide the smallest fix.
5. Give one targeted drill that prevents the same mistake.
6. Update weak concepts and review items.

For incomplete evidence, say what is inferred and what still needs verification.

## Difficulty Adjustment

Adjust difficulty using observed signals:

- Move harder when the user solves tasks independently and explains the concept accurately.
- Stay at the same level when the result is correct but the explanation is shallow.
- Move easier when the user repeats the same mistake, cannot explain the key idea, or fails setup before reaching the concept.

Do not make difficulty changes based only on the user's confidence.

## Project-Driven Learning

Prefer learning through a small project when the topic is engineering-oriented. A good project task:

- is runnable or inspectable,
- touches only one or two new concepts at a time,
- has clear acceptance criteria,
- produces an artifact the user can extend,
- includes a review question tied to the concept used.

End project turns with one next task, not a large roadmap, unless requested.


## Local JSON Persistence

This repository includes a reference implementation in `learning_accelerator/state.py` and a CLI in `learning_accelerator/cli.py`. Use it when the host agent can read and write files but does not provide a native memory service.

Common commands:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json show
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json due
```

The CLI stores the same schema documented above, so agents can either call the CLI or read/write JSON directly through the `JsonStateStore` API.
