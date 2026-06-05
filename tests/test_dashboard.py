from __future__ import annotations

from learning_accelerator.dashboard import render_dashboard


def test_render_dashboard_shows_learning_state_sections():
    summary = {
        "learning_goal": "Learn FastAPI",
        "target_outcome": "Build a RAG API",
        "current_topic": "dependency injection",
        "level": "beginner",
        "weak_concepts": ["Depends"],
        "priority_reviews": [
            {
                "concept": "Depends",
                "prompt": "Explain Depends.",
                "priority": 68,
                "due_at": "2026-06-04",
                "strength": 0.4,
            }
        ],
        "concept_progress": {
            "Depends": {
                "strength": 0.4,
                "attempts": 2,
                "correct_streak": 0,
                "failure_count": 1,
                "next_due_at": "2026-06-04",
            }
        },
        "current_tasks": [{"name": "Implement one route", "status": "pending"}],
        "current_difficulty": 2,
        "next_adjustment": "same",
    }

    output = render_dashboard(summary)

    assert "Learning Accelerator Dashboard" in output
    assert "Goal: Learn FastAPI" in output
    assert "Outcome: Build a RAG API" in output
    assert "Topic: dependency injection (beginner)" in output
    assert "Depends | priority 68 | due 2026-06-04 | strength 0.4" in output
    assert "Depends | strength 0.4 | attempts 2 | streak 0 | failures 1 | next 2026-06-04" in output
    assert "Implement one route" in output
    assert "Difficulty: 2 | Next adjustment: same" in output


def test_render_dashboard_handles_empty_state():
    output = render_dashboard({
        "learning_goal": "",
        "target_outcome": "",
        "current_topic": "",
        "level": "beginner",
        "weak_concepts": [],
        "priority_reviews": [],
        "concept_progress": {},
        "current_tasks": [],
        "current_difficulty": 1,
        "next_adjustment": "same",
    })

    assert "Goal: unset" in output
    assert "Priority Reviews" in output
    assert "No priority reviews." in output
    assert "No concept progress yet." in output
