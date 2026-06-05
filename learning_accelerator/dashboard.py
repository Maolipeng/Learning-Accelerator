"""Plain-text dashboard rendering for Learning Accelerator state."""

from __future__ import annotations

from typing import Any


def _value(value: Any, fallback: str = "unset") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text or fallback


def _section(title: str) -> list[str]:
    return ["", title, "-" * len(title)]


def render_dashboard(summary: dict[str, Any]) -> str:
    """Render a deterministic terminal dashboard from ``JsonStateStore.summary``."""

    goal = _value(summary.get("learning_goal"))
    outcome = _value(summary.get("target_outcome"))
    topic = _value(summary.get("current_topic"))
    level = _value(summary.get("level"), "unknown")
    weak_concepts = summary.get("weak_concepts") or []
    priority_reviews = summary.get("priority_reviews") or []
    concept_progress = summary.get("concept_progress") or {}
    current_tasks = summary.get("current_tasks") or []

    lines = [
        "Learning Accelerator Dashboard",
        "==============================",
        f"Goal: {goal}",
        f"Outcome: {outcome}",
        f"Topic: {topic} ({level})",
        f"Difficulty: {summary.get('current_difficulty', 1)} | Next adjustment: {summary.get('next_adjustment', 'same')}",
        f"Weak concepts: {', '.join(str(item) for item in weak_concepts) if weak_concepts else 'none'}",
    ]

    lines.extend(_section("Priority Reviews"))
    if priority_reviews:
        for item in priority_reviews:
            lines.append(
                f"{_value(item.get('concept'))} | priority {item.get('priority', 0)} | "
                f"due {_value(item.get('due_at'))} | strength {item.get('strength', 'unknown')}"
            )
            prompt = _value(item.get("prompt"), "")
            if prompt:
                lines.append(f"  prompt: {prompt}")
    else:
        lines.append("No priority reviews.")

    lines.extend(_section("Concept Progress"))
    if concept_progress:
        for concept in sorted(concept_progress):
            item = concept_progress[concept]
            lines.append(
                f"{concept} | strength {item.get('strength', 'unknown')} | "
                f"attempts {item.get('attempts', 0)} | streak {item.get('correct_streak', 0)} | "
                f"failures {item.get('failure_count', 0)} | next {_value(item.get('next_due_at'))}"
            )
    else:
        lines.append("No concept progress yet.")

    lines.extend(_section("Current Tasks"))
    if current_tasks:
        for task in current_tasks:
            lines.append(f"{_value(task.get('name'))} | {task.get('status', 'pending')}")
    else:
        lines.append("No current tasks.")

    return "\n".join(lines) + "\n"
