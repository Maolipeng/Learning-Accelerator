# General Learning OS Protocol

Load this reference when the user asks for dynamic learning, review memory, spaced repetition, task-driven learning, exercise generation, mistake analysis, or difficulty adjustment.

## Operating Modes

Classify each turn into one primary mode:

- `onboarding`: discover goals, learning domain, background, known skills, constraints, and target task/project.
- `concept`: teach one concept with analogy, demo or example, practical use, pitfalls, and recall.
- `project`: guide a concrete task or project step and tie it back to concepts.
- `practice`: generate exercises or evaluate the user's answer.
- `review`: run spaced repetition and memory recall.
- `debug`: analyze code, logs, test failures, wrong answers, drafts, attempts, or other learning mistakes.
- `calibration`: adjust difficulty based on observed performance.

## Learning State Schema

Use this shape when persistent memory, the bundled `learning_accelerator` JSON store, or a host-provided state store exists. If no storage exists, include a compact version in the answer under `学习状态` and `状态更新`.

```json
{
  "schema_version": 1,
  "learner_profile": {
    "learning_domain": "general|technology|language|exam|writing|communication|fitness|finance|custom",
    "known_stack": [],
    "known_skills": [],
    "preferred_language": "zh-CN",
    "learning_goal": "",
    "target_outcome": "",
    "target_project": "",
    "constraints": [],
    "experience_level": "unknown|no_programming|beginner|intermediate|advanced"
  },
  "topic_state": {
    "current_topic": "",
    "level": "beginner|intermediate|advanced",
    "mastered_concepts": [],
    "weak_concepts": [],
    "concept_progress": {
      "concept name": {
        "concept": "",
        "strength": 0.5,
        "attempts": 0,
        "correct_streak": 0,
        "last_reviewed_at": "YYYY-MM-DD",
        "next_due_at": "YYYY-MM-DD",
        "failure_count": 0
      }
    },
    "misconceptions": [],
    "open_questions": []
  },
  "practice_state": {
    "exercise_specs": [
      {
        "id": "stable-exercise-id",
        "topic": "",
        "concepts": [],
        "difficulty": "easy|normal|stretch",
        "goal": "",
        "task": "",
        "input": "",
        "expected_output": "",
        "constraints": [],
        "evaluation_criteria": [],
        "hint": "",
        "created_at": "YYYY-MM-DD"
      }
    ],
    "attempt_records": [
      {
        "id": "stable-attempt-id",
        "exercise_id": "stable-exercise-id",
        "user_answer": "",
        "result": "pass|partial|fail",
        "score": 0,
        "mistake_type": "",
        "feedback": "",
        "concepts_to_review": [],
        "created_at": "YYYY-MM-DD"
      }
    ],
    "completed_exercises": [],
    "failed_exercises": [],
    "current_tasks": [],
    "current_project_tasks": [],
    "last_code_errors": []
  },
  "review_state": {
    "due_items": [
      {
        "id": "stable-review-id",
        "concept": "",
        "prompt": "",
        "source": "manual",
        "result": "incorrect|fuzzy|correct|second_correct|third_correct",
        "created_at": "YYYY-MM-DD",
        "due_at": "YYYY-MM-DD"
      }
    ],
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

Review items should have stable `id` values derived from concept and prompt. When the same concept/prompt pair is scheduled again, update the existing pending review instead of appending a duplicate. When the user completes a review, move the attempt into `review_history`; optionally schedule the next interval based on the result.

Do not ask the user to review everything. Select 2-5 high-value items:

- recently learned core concepts,
- repeated mistakes,
- concepts required by the next task or project step,
- concepts the user could not explain back.

Track each concept with `ConceptProgress` so review scheduling does not depend only on conversation memory. `strength` is a 0.0-1.0 estimate, `correct_streak` controls interval growth, `failure_count` keeps repeated weak spots visible, and `next_due_at` lets agents rank what to review first.

Use `review-priority` when a turn needs a short review set. It should prefer due items, weak concepts, lower-strength concepts, and concepts with repeated failures.

## Exercise Generation

Generate exercises with:

- `goal`: what concept it tests,
- `task`: what to build or answer,
- `input/output`: concrete expected behavior when applicable,
- `constraints`: what must or must not be used,
- `evaluation`: how the answer will be judged,
- `hint`: one optional hint, hidden until needed.

When local persistence is available, convert each generated exercise into an `ExerciseSpec` before presenting it as durable practice. The LLM may draft the task, hint, and evaluation text, but Python owns the stable id, storage, and later lookup. An `ExerciseSpec` should include:

- `topic`: the current learning topic,
- `concepts`: one or more tested concepts,
- `difficulty`: `easy`, `normal`, or `stretch`,
- `goal`: the learning purpose,
- `task`: the learner-facing instruction,
- `input` and `expected_output`: concrete behavior when applicable,
- `constraints`: required boundaries,
- `evaluation_criteria`: how the answer will be judged,
- `hint`: one optional hint.

Use three levels:

- `easy`: direct application of the just-learned concept.
- `normal`: combine the concept with one familiar idea.
- `stretch`: apply it in a realistic project-like scenario.

After the learner answers, persist an `AttemptRecord`. The evaluator can be an LLM, a human, or a deterministic checker, but the result should be structured:

- `exercise_id`: the related `ExerciseSpec`,
- `user_answer`: the answer or attempt summary,
- `result`: `pass`, `partial`, or `fail`,
- `score`: 0-100,
- `mistake_type`: the misconception category when useful,
- `feedback`: concise evaluator feedback,
- `concepts_to_review`: concepts that should feed review scheduling.

Use `pass` attempts as positive difficulty evidence. Treat `partial` and `fail` as weak-concept evidence and schedule the listed concepts for review.

Each `AttemptRecord` should also update `ConceptProgress`: `pass` increases strength and streak, while `partial` or `fail` resets the streak, increments failures, lowers strength, and makes the concept due immediately.

## Error Analysis

When the user provides code, logs, a failing test, a wrong answer, a draft, a recording summary, or a failed attempt:

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

Useful evidence signals include:

- `exercise_completed`
- `exercise_failed`
- `recall_correct`
- `recall_incorrect`
- `explain_correct`
- `explain_fuzzy`
- `setup_failed`

## Task-Driven Learning

Prefer learning through a small concrete task. For engineering topics this may be a runnable project; for non-technical topics it may be a drill, worksheet, writing revision, speaking practice, mock exam question, or habit log. A good task:

- is runnable, inspectable, answerable, or observable,
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
python -m learning_accelerator.cli --state-file .learning/state.json onboarding --domain language
python -m learning_accelerator.cli --state-file .learning/state.json domain-template language
python -m learning_accelerator.cli --state-file .learning/state.json profile --domain language --known-skill "中文拼音" --goal "通过日语 N5"
python -m learning_accelerator.cli --state-file .learning/state.json show
python -m learning_accelerator.cli --state-file .learning/state.json summary
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json concept-progress
python -m learning_accelerator.cli --state-file .learning/state.json due
python -m learning_accelerator.cli --state-file .learning/state.json review-priority --limit 3
python -m learning_accelerator.cli --state-file .learning/state.json review-complete "<review-id-from-due>" --result correct
python -m learning_accelerator.cli --state-file .learning/state.json task add "每天复习 5 个假名"
python -m learning_accelerator.cli --state-file .learning/state.json exercise complete "Build /ask mock API" --concept "FastAPI route"
python -m learning_accelerator.cli --state-file .learning/state.json exercise-generate --topic "FastAPI dependencies" --concept "dependency injection" --difficulty normal --task "Explain why Depends is not middleware." --evaluation "Mentions per-request dependency resolution"
python -m learning_accelerator.cli --state-file .learning/state.json exercise-show "<exercise-id>"
python -m learning_accelerator.cli --state-file .learning/state.json attempt record "<exercise-id>" --answer "Depends wraps every request like middleware." --result partial --score 45 --mistake-type concept_confusion --feedback "Confused dependency resolution with middleware." --review-concept "dependency injection"
```

The CLI stores the same schema documented above, so agents can either call the CLI or read/write JSON directly through the `JsonStateStore` API.

Use `dashboard` when a human wants a terminal UI view of the current learning state. It renders goal, outcome, topic, weak concepts, priority reviews, concept progress, current tasks, and difficulty without requiring the user to inspect JSON.

Use `tui` when a human wants an interactive terminal session. It can show dashboard, priority reviews, concept progress, due reviews, and add current tasks while preserving the same JSON state model.
