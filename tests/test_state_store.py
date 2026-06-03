from __future__ import annotations

import json
from datetime import date

import pytest

from learning_accelerator.state import JsonStateStore, LearningStateError, create_review_item


def test_store_loads_default_when_file_is_absent(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    state = store.load()

    assert state["schema_version"] == 1
    assert state["learner_profile"]["preferred_language"] == "zh-CN"
    assert state["topic_state"]["level"] == "beginner"


def test_profile_topic_and_concept_updates_are_persisted(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    store.reset()
    store.update_profile(
        known_stack=["JavaScript", "React"],
        experience_level="intermediate",
        learning_goal="Build AI tools",
        target_project="RAG notebook",
        constraint="30 minutes per day",
    )
    store.set_topic("FastAPI dependencies", level="intermediate")
    state = store.record_concept("dependency injection", "weak")
    state = store.record_concept("path operation", "mastered")

    assert state["learner_profile"]["known_stack"] == ["JavaScript", "React"]
    assert state["learner_profile"]["experience_level"] == "intermediate"
    assert state["learner_profile"]["constraints"] == ["30 minutes per day"]
    assert state["topic_state"]["current_topic"] == "FastAPI dependencies"
    assert state["topic_state"]["level"] == "intermediate"
    assert state["topic_state"]["weak_concepts"] == ["dependency injection"]
    assert state["topic_state"]["mastered_concepts"] == ["path operation"]


def test_profile_supports_general_learning_domain_and_known_skills(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    state = store.update_profile(
        learning_domain="language",
        known_skills=["中文写作", "基础拼音"],
        experience_level="beginner",
        learning_goal="学习日语",
        target_project="通过 N5",
    )

    assert state["learner_profile"]["learning_domain"] == "language"
    assert state["learner_profile"]["known_skills"] == ["中文写作", "基础拼音"]
    assert state["learner_profile"]["learning_goal"] == "学习日语"

    summary = store.summary()
    prompt_context = store.prompt_context()
    assert summary["learning_domain"] == "language"
    assert summary["known_skills"] == ["中文写作", "基础拼音"]
    assert "学习领域：language" in prompt_context
    assert "已知技能：中文写作, 基础拼音" in prompt_context


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
    assert due_items[0]["id"]


def test_duplicate_review_updates_existing_item_instead_of_appending(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    first = store.add_review("dependency injection", "Explain Depends.", result="incorrect")
    second = store.add_review("dependency injection", "Explain Depends.", result="correct")

    next_items = second["review_state"]["next_review_items"]
    assert len(next_items) == 1
    assert next_items[0]["id"] == first["review_state"]["next_review_items"][0]["id"]
    assert next_items[0]["result"] == "correct"


def test_complete_review_moves_item_to_history_and_reschedules_when_requested(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    state = store.add_review("dependency injection", "Explain Depends.", result="incorrect")
    review_id = state["review_state"]["next_review_items"][0]["id"]

    completed = store.complete_review(review_id, result="correct", reschedule=True)

    review_state = completed["review_state"]
    assert review_state["next_review_items"][0]["id"] == review_id
    assert review_state["next_review_items"][0]["due_at"] > review_state["next_review_items"][0]["created_at"]
    assert review_state["review_history"][0]["id"] == review_id
    assert review_state["review_history"][0]["completed_result"] == "correct"
    assert review_state["review_history"][0]["completed_at"]


def test_complete_review_can_archive_without_rescheduling(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    state = store.add_review("path operation", "What is a route handler?", result="incorrect")
    review_id = state["review_state"]["next_review_items"][0]["id"]

    completed = store.complete_review(review_id, result="correct", reschedule=False)

    assert completed["review_state"]["next_review_items"] == []
    assert completed["review_state"]["review_history"][0]["id"] == review_id


def test_record_exercise_tracks_success_failure_and_difficulty_evidence(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")

    state = store.record_exercise(
        "Build /ask mock API",
        status="completed",
        concepts=["FastAPI route", "Pydantic schema"],
        notes="Solved independently",
    )
    state = store.record_exercise(
        "Explain dependency injection",
        status="failed",
        concepts=["dependency injection"],
        notes="Confused Depends with middleware",
    )

    assert state["practice_state"]["completed_exercises"][0]["name"] == "Build /ask mock API"
    assert state["practice_state"]["failed_exercises"][0]["name"] == "Explain dependency injection"
    assert state["difficulty_state"]["evidence"][-1]["signal"] == "exercise_failed"


def test_record_evidence_adjusts_difficulty_from_recent_signals(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    store.record_evidence("exercise_completed", "Solved task independently")
    state = store.record_evidence("explain_correct", "Explained the concept clearly")

    assert state["difficulty_state"]["next_adjustment"] == "harder"
    assert state["difficulty_state"]["current_difficulty"] == 2

    store.record_evidence("exercise_failed", "Failed setup")
    state = store.record_evidence("recall_incorrect", "Could not explain the key idea")

    assert state["difficulty_state"]["next_adjustment"] == "easier"
    assert state["difficulty_state"]["current_difficulty"] == 1


def test_summary_and_prompt_context_are_agent_friendly(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    store.update_profile(learning_goal="Learn FastAPI", target_project="RAG API")
    store.set_topic("dependency injection", level="beginner")
    store.record_concept("Depends", "weak")
    store.add_review("Depends", "Explain Depends.", result="incorrect")

    summary = store.summary(on_date="2999-01-01")
    prompt_context = store.prompt_context(on_date="2999-01-01")

    assert summary["learning_goal"] == "Learn FastAPI"
    assert summary["current_topic"] == "dependency injection"
    assert summary["weak_concepts"] == ["Depends"]
    assert summary["due_reviews"][0]["concept"] == "Depends"
    assert "当前学习目标：Learn FastAPI" in prompt_context
    assert "今天需要复习：Depends" in prompt_context


def test_legacy_state_without_schema_version_is_migrated(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps({
            "learner_profile": {"learning_goal": "Learn Python"},
            "topic_state": {"level": "beginner"},
        }),
        encoding="utf-8",
    )
    store = JsonStateStore(state_file)

    state = store.load()

    assert state["schema_version"] == 1
    assert state["learner_profile"]["learning_goal"] == "Learn Python"


def test_invalid_state_raises_helpful_error(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"topic_state": {"level": "expert"}}', encoding="utf-8")
    store = JsonStateStore(state_file)

    with pytest.raises(LearningStateError, match="topic_state.level"):
        store.load()
