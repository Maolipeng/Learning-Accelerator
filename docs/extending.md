# Extending Learning Accelerator

This guide explains safe Extension Points for adapting the Learning Accelerator without breaking existing agents.

## Do Not Break

Keep these contracts stable:

- `schema_version` remains `1` until a breaking migration is required.
- Existing top-level state keys stay present: `learner_profile`, `topic_state`, `practice_state`, `review_state`, `difficulty_state`.
- Existing CLI command names remain available.
- `JsonStateStore.load()` continues to migrate older state files.
- `prompt-context` stays compact enough to paste into another agent.
- `tui` remains a standard-library interactive loop and should not require optional terminal packages.

## Domain Templates

`DOMAIN_TEMPLATES` in `learning_accelerator.state` defines onboarding questions, focus areas, practice types, and review strategy by domain.

To add a domain:

1. Add a new key such as `music`, `sales`, or `medicine`.
2. Include `domain`, `focus_areas`, `practice_types`, `review_strategy`, and `onboarding_questions`.
3. Add tests that `domain-template <domain>` returns the new template.

Keep templates short. They should guide the agent, not become a full curriculum.

## ExerciseSpec Extensions

`ExerciseSpec` is the durable shape for generated practice. Add optional fields when a domain needs more structure, for example:

- `rubric`,
- `time_limit_minutes`,
- `sample_answer`,
- `materials`,
- `input_files`.

Do not remove or rename `id`, `topic`, `concepts`, `difficulty`, `goal`, `task`, or `created_at`.

## AttemptRecord Extensions

`AttemptRecord` stores evaluator output. Useful optional extensions include:

- `grader`,
- `raw_feedback`,
- `artifact_path`,
- `retry_of`,
- `confidence`.

Keep `result` limited to `pass`, `partial`, and `fail` unless the scheduler is updated at the same time.

## ConceptProgress Extensions

`ConceptProgress` tracks one concept over time. Current fields are:

- `strength`,
- `attempts`,
- `correct_streak`,
- `last_reviewed_at`,
- `next_due_at`,
- `failure_count`.

Possible extensions:

- `last_mistake_type`,
- `related_concepts`,
- `review_interval_days`,
- `source_exercises`.

If you change strength or due-date behavior, update `priority_reviews`, tests, and `references/learning_os_protocol.md`.

## Review Strategy

The current Review Strategy prefers:

1. due review items,
2. weak concepts,
3. lower `strength`,
4. repeated failures.

For more advanced scheduling, add behavior behind `priority_reviews()` rather than requiring agents to sort raw review items themselves.

## Adding CLI Commands

When adding a command:

1. Add a failing test in `tests/test_cli.py`.
2. Add parser wiring in `learning_accelerator.cli`.
3. Print JSON for machine-readable outputs.
4. Update `docs/api.md`, `README.md`, and `references/learning_os_protocol.md`.

For interactive commands, inject input/output functions in tests so the command loop never blocks CI.

## Adding Schema Fields

Update both:

- `schemas/learning_state.schema.json`
- `references/learning_os_protocol.md`

Prefer optional fields and keep `additionalProperties` enabled for forward compatibility.
