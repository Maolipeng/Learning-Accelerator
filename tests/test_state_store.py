from __future__ import annotations

from datetime import date

import pytest

from learning_accelerator.state import JsonStateStore, LearningStateError, create_review_item


def test_store_loads_default_when_file_is_absent(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    state = store.load()

    assert state["learner_profile"]["preferred_language"] == "zh-CN"
    assert state["topic_state"]["level"] == "beginner"


def test_profile_topic_and_concept_updates_are_persisted(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    store.reset()
    store.update_profile(
        known_stack=["JavaScript", "React"],
        learning_goal="Build AI tools",
        target_project="RAG notebook",
        constraint="30 minutes per day",
    )
    store.set_topic("FastAPI dependencies", level="intermediate")
    state = store.record_concept("dependency injection", "weak")
    state = store.record_concept("path operation", "mastered")

    assert state["learner_profile"]["known_stack"] == ["JavaScript", "React"]
    assert state["learner_profile"]["constraints"] == ["30 minutes per day"]
    assert state["topic_state"]["current_topic"] == "FastAPI dependencies"
    assert state["topic_state"]["level"] == "intermediate"
    assert state["topic_state"]["weak_concepts"] == ["dependency injection"]
    assert state["topic_state"]["mastered_concepts"] == ["path operation"]


def test_recording_mastered_concept_removes_it_from_weak_list(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    store.record_concept("decorators", "weak")
    state = store.record_concept("decorators", "mastered")

    assert "decorators" in state["topic_state"]["mastered_concepts"]
    assert "decorators" not in state["topic_state"]["weak_concepts"]


def test_review_item_intervals_and_due_filter(tmp_path):
    item = create_review_item(
        "Pydantic model",
        "Explain request validation.",
        result="second_correct",
        today=date(2026, 6, 3),
    )
    assert item["due_at"] == "2026-06-06"

    store = JsonStateStore(tmp_path / "state.json")
    store.add_review("async IO", "Why avoid blocking calls?", result="incorrect")

    due_items = store.due_reviews(on_date="2999-01-01")
    assert due_items[0]["concept"] == "async IO"


def test_invalid_state_raises_helpful_error(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"topic_state": {"level": "expert"}}', encoding="utf-8")
    store = JsonStateStore(state_file)

    with pytest.raises(LearningStateError, match="topic_state.level"):
        store.load()
