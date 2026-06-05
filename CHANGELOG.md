# Changelog

All notable changes to Learning Accelerator are documented here.

## Unreleased

- No unreleased changes yet.

## v1.6.0

### Added

- Added structured `ExerciseSpec` persistence for durable generated practice.
- Added `AttemptRecord` persistence for learner answers, evaluator results, scores, mistake type, and feedback.
- Added `ConceptProgress` tracking for strength, attempts, correct streak, failure count, and next due date.
- Added `priority_reviews()` and `review-priority` for ranking due review items.
- Added `concept-progress`, `exercise-generate`, `exercise-show`, and `attempt record` CLI commands.
- Added zero-dependency terminal `dashboard` command for human-readable learning state.
- Added standard-library interactive `tui` command for dashboard, reviews, concept progress, due reviews, and task creation.
- Added `schemas/learning_state.schema.json`.
- Added `docs/api.md` and `docs/extending.md`.

### Changed

- Review completion now updates concept-level progress.
- Structured attempts now update weak concepts, review items, difficulty evidence, and concept progress.
- `prompt-context` includes priority review concepts.

## v1.2.0

### Added

- General Learning OS skill package with `SKILL.md`, `SYSTEM_PROMPT.md`, platform guides, examples, and CLI persistence.
- Local JSON persistence through `JsonStateStore`.
- Spaced repetition primitives through review items and review completion.
- Basic difficulty evidence and adjustment.
- Multi-domain onboarding templates for technology, language, exam, writing, communication, and general learning.
