"""Persistent learning-state primitives for the Learning Accelerator skill.

The module intentionally uses only the Python standard library so the CLI can
run in constrained agent environments without dependency installation.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

DEFAULT_STATE: dict[str, Any] = {
    "learner_profile": {
        "known_stack": [],
        "preferred_language": "zh-CN",
        "learning_goal": "",
        "target_project": "",
        "constraints": [],
    },
    "topic_state": {
        "current_topic": "",
        "level": "beginner",
        "mastered_concepts": [],
        "weak_concepts": [],
        "misconceptions": [],
        "open_questions": [],
    },
    "practice_state": {
        "completed_exercises": [],
        "failed_exercises": [],
        "current_project_tasks": [],
        "last_code_errors": [],
    },
    "review_state": {
        "due_items": [],
        "review_history": [],
        "next_review_items": [],
    },
    "difficulty_state": {
        "current_difficulty": 1,
        "evidence": [],
        "next_adjustment": "same",
    },
}

REVIEW_INTERVALS_BY_RESULT = {
    "correct": 1,
    "second_correct": 3,
    "third_correct": 7,
    "incorrect": 0,
    "fuzzy": 0,
}


class LearningStateError(ValueError):
    """Raised when persisted learning-state data is malformed."""


def today_iso() -> str:
    """Return today's date in ISO-8601 format."""

    return date.today().isoformat()


def _deep_merge(default: dict[str, Any], loaded: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(default)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _ensure_list(value: Any, field_name: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise LearningStateError(f"{field_name} must be a list")
    return value


def create_review_item(
    concept: str,
    prompt: str,
    result: str = "correct",
    source: str = "manual",
    today: date | None = None,
) -> dict[str, Any]:
    """Create a review item using the default spaced-repetition intervals."""

    if result not in REVIEW_INTERVALS_BY_RESULT:
        allowed = ", ".join(sorted(REVIEW_INTERVALS_BY_RESULT))
        raise LearningStateError(f"result must be one of: {allowed}")
    base_day = today or date.today()
    due_day = base_day + timedelta(days=REVIEW_INTERVALS_BY_RESULT[result])
    return {
        "concept": concept,
        "prompt": prompt,
        "source": source,
        "result": result,
        "created_at": base_day.isoformat(),
        "due_at": due_day.isoformat(),
    }


@dataclass
class JsonStateStore:
    """Read and write Learning Accelerator state in a local JSON file."""

    path: Path

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()

    def load(self) -> dict[str, Any]:
        """Load state from disk, returning the default schema if absent."""

        if not self.path.exists():
            return copy.deepcopy(DEFAULT_STATE)
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LearningStateError(f"Invalid JSON in {self.path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise LearningStateError("Learning state root must be an object")
        return self.validate(_deep_merge(DEFAULT_STATE, raw))

    def save(self, state: dict[str, Any]) -> dict[str, Any]:
        """Validate and persist state, creating parent directories as needed."""

        validated = self.validate(state)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return validated

    def reset(self) -> dict[str, Any]:
        """Overwrite the store with a fresh default state."""

        return self.save(copy.deepcopy(DEFAULT_STATE))

    def update_profile(
        self,
        *,
        known_stack: list[str] | None = None,
        preferred_language: str | None = None,
        learning_goal: str | None = None,
        target_project: str | None = None,
        constraint: str | None = None,
    ) -> dict[str, Any]:
        """Update learner profile fields and persist the result."""

        state = self.load()
        profile = state["learner_profile"]
        if known_stack is not None:
            profile["known_stack"] = known_stack
        if preferred_language:
            profile["preferred_language"] = preferred_language
        if learning_goal is not None:
            profile["learning_goal"] = learning_goal
        if target_project is not None:
            profile["target_project"] = target_project
        if constraint:
            constraints = _ensure_list(profile.get("constraints"), "constraints")
            if constraint not in constraints:
                constraints.append(constraint)
            profile["constraints"] = constraints
        return self.save(state)

    def set_topic(self, topic: str, level: str | None = None) -> dict[str, Any]:
        """Set the active learning topic and optional level."""

        state = self.load()
        state["topic_state"]["current_topic"] = topic
        if level:
            state["topic_state"]["level"] = level
        return self.save(state)

    def record_concept(self, concept: str, status: str) -> dict[str, Any]:
        """Record a concept as mastered or weak, keeping lists de-duplicated."""

        if status not in {"mastered", "weak"}:
            raise LearningStateError("status must be 'mastered' or 'weak'")
        state = self.load()
        target_key = "mastered_concepts" if status == "mastered" else "weak_concepts"
        other_key = "weak_concepts" if status == "mastered" else "mastered_concepts"
        target = _ensure_list(state["topic_state"].get(target_key), target_key)
        other = _ensure_list(state["topic_state"].get(other_key), other_key)
        if concept not in target:
            target.append(concept)
        state["topic_state"][target_key] = target
        state["topic_state"][other_key] = [item for item in other if item != concept]
        return self.save(state)

    def add_review(
        self,
        concept: str,
        prompt: str,
        result: str = "correct",
        source: str = "manual",
    ) -> dict[str, Any]:
        """Add a scheduled review item and persist the state."""

        state = self.load()
        item = create_review_item(concept, prompt, result=result, source=source)
        next_items = _ensure_list(state["review_state"].get("next_review_items"), "next_review_items")
        next_items.append(item)
        state["review_state"]["next_review_items"] = next_items
        return self.save(state)

    def due_reviews(self, on_date: str | None = None) -> list[dict[str, Any]]:
        """Return review items whose due date is on or before ``on_date``."""

        target = on_date or today_iso()
        state = self.load()
        review_state = state["review_state"]
        candidates = []
        candidates.extend(_ensure_list(review_state.get("due_items"), "due_items"))
        candidates.extend(_ensure_list(review_state.get("next_review_items"), "next_review_items"))
        return [item for item in candidates if str(item.get("due_at", "")) <= target]

    @staticmethod
    def validate(state: dict[str, Any]) -> dict[str, Any]:
        """Validate the top-level schema and normalize missing keys."""

        if not isinstance(state, dict):
            raise LearningStateError("Learning state must be a dictionary")
        normalized = _deep_merge(DEFAULT_STATE, state)
        for section in DEFAULT_STATE:
            if section not in normalized or not isinstance(normalized[section], dict):
                raise LearningStateError(f"{section} must be an object")
        topic = normalized["topic_state"]
        if topic.get("level") not in {"beginner", "intermediate", "advanced"}:
            raise LearningStateError("topic_state.level must be beginner, intermediate, or advanced")
        difficulty = normalized["difficulty_state"].get("current_difficulty")
        if not isinstance(difficulty, int) or not 1 <= difficulty <= 5:
            raise LearningStateError("difficulty_state.current_difficulty must be an integer from 1 to 5")
        return normalized
