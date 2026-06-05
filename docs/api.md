# Learning Accelerator API

This document describes the stable local API surface for agents and developers. The runtime intentionally uses only the Python standard library.

## State Store

`JsonStateStore` in `learning_accelerator.state` is the main API. It reads, migrates, validates, and writes the JSON state file.

Common methods:

- `load()` returns the current state or the default schema when the file does not exist.
- `save(state)` validates and writes state.
- `reset()` overwrites the file with the default state.
- `summary(on_date=None)` returns an agent-friendly state snapshot.
- `prompt_context(on_date=None)` renders a compact text summary for another agent.

## Profile and Topics

- `update_profile(...)` records learning domain, known skills, experience level, goals, outcomes, projects, and constraints.
- `set_topic(topic, level=None)` sets the active topic.
- `record_concept(concept, status)` records a concept as `mastered` or `weak`.
- `concept_progress` lives under `topic_state` and tracks per-concept strength, attempts, streaks, due date, and failures.

## Review API

- `create_review_item(concept, prompt, result="correct", source="manual")` creates a deterministic review item.
- `add_review(concept, prompt, result="correct", source="manual")` persists a pending review.
- `complete_review(review_id, result, reschedule=True, notes="")` archives a review attempt and optionally schedules the next interval.
- `due_reviews(on_date=None)` returns due review items.
- `priority_reviews(on_date=None, limit=5)` ranks due items by weak status, concept strength, and failure count.

## Practice API

- `create_exercise_spec(...)` builds a structured `ExerciseSpec`.
- `add_exercise_spec(spec)` persists an exercise spec and de-duplicates by id.
- `exercise_spec(exercise_id)` returns one persisted exercise.
- `record_attempt(exercise_id, user_answer, result, score, mistake_type="", feedback="", concepts_to_review=None)` persists an `AttemptRecord`.

`record_attempt` also updates review items, weak concepts, `concept_progress`, and difficulty evidence.

Legacy practice methods remain available:

- `record_exercise(name, status, concepts=None, notes="")`
- `add_task(name, notes="")`

## CLI Commands

Core commands:

```bash
python -m learning_accelerator.cli version
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json show
python -m learning_accelerator.cli --state-file .learning/state.json summary
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
```

`version` prints the package version and persisted state schema version as JSON.

`dashboard` is a zero-dependency terminal UI. It renders the same summary data as readable sections instead of JSON.

`tui` runs an interactive menu loop for dashboard, priority reviews, concept progress, due reviews, and adding tasks.

Review and progress:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json due
python -m learning_accelerator.cli --state-file .learning/state.json review-priority --limit 3
python -m learning_accelerator.cli --state-file .learning/state.json review-complete "<review-id>" --result correct
python -m learning_accelerator.cli --state-file .learning/state.json concept-progress
```

Structured practice:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json exercise-generate --topic "FastAPI" --concept "dependency injection" --difficulty normal --task "Explain Depends."
python -m learning_accelerator.cli --state-file .learning/state.json exercise-show "<exercise-id>"
python -m learning_accelerator.cli --state-file .learning/state.json attempt record "<exercise-id>" --answer "..." --result partial --score 45 --review-concept "dependency injection"
```

## State Schema

The persisted state schema is documented in `references/learning_os_protocol.md` and machine-readable in `schemas/learning_state.schema.json`.

The schema is intentionally permissive with `additionalProperties` so future agents can add metadata without breaking older clients. Stable fields should remain backward compatible.

## Error Handling

Invalid state raises `LearningStateError`. Examples:

- invalid JSON,
- non-object root state,
- invalid topic level,
- invalid difficulty value,
- missing exercise id,
- score outside 0-100.

Agents should catch `LearningStateError` when embedding the Python API directly and surface a short corrective message to the user.
