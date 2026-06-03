from __future__ import annotations

import json

from learning_accelerator.cli import main


def test_cli_profile_topic_review_and_due(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "profile",
        "--known-stack",
        "TypeScript",
        "React",
        "--experience-level",
        "intermediate",
        "--goal",
        "Learn FastAPI",
    ]) == 0
    assert main(["--state-file", str(state_file), "topic", "FastAPI", "--level", "beginner"]) == 0
    assert main(["--state-file", str(state_file), "concept", "weak", "dependency injection"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "review",
        "dependency injection",
        "Explain Depends in one sentence.",
        "--result",
        "incorrect",
    ]) == 0
    assert main(["--state-file", str(state_file), "due", "--date", "2999-01-01"]) == 0

    output = capsys.readouterr().out.strip().splitlines()
    due_json_start = next(i for i in range(len(output) - 1, -1, -1) if output[i] == "[")
    due_items = json.loads("\n".join(output[due_json_start:]))
    assert due_items[0]["concept"] == "dependency injection"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["learner_profile"]["experience_level"] == "intermediate"


def test_cli_profile_accepts_general_learning_background(tmp_path):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "profile",
        "--domain",
        "language",
        "--known-skill",
        "中文写作",
        "--known-skill",
        "基础拼音",
        "--experience-level",
        "beginner",
        "--goal",
        "学习日语",
    ]) == 0
    assert main(["--state-file", str(state_file), "summary"]) == 0

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["learner_profile"]["learning_domain"] == "language"
    assert state["learner_profile"]["known_skills"] == ["中文写作", "基础拼音"]


def test_cli_review_complete_exercise_difficulty_and_context(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main(["--state-file", str(state_file), "profile", "--goal", "Learn FastAPI"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "review",
        "dependency injection",
        "Explain Depends.",
        "--result",
        "incorrect",
    ]) == 0
    state = json.loads(state_file.read_text(encoding="utf-8"))
    review_id = state["review_state"]["next_review_items"][0]["id"]

    assert main([
        "--state-file",
        str(state_file),
        "review-complete",
        review_id,
        "--result",
        "correct",
        "--no-reschedule",
    ]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "exercise",
        "complete",
        "Build /ask mock API",
        "--concept",
        "FastAPI route",
        "--notes",
        "Solved independently",
    ]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "evidence",
        "explain_correct",
        "Explained route/schema boundary",
    ]) == 0
    assert main(["--state-file", str(state_file), "summary", "--date", "2999-01-01"]) == 0
    assert main(["--state-file", str(state_file), "prompt-context", "--date", "2999-01-01"]) == 0

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["review_state"]["next_review_items"] == []
    assert state["review_state"]["review_history"][0]["completed_result"] == "correct"
    assert state["practice_state"]["completed_exercises"][0]["name"] == "Build /ask mock API"

    output = capsys.readouterr().out
    assert '"learning_goal": "Learn FastAPI"' in output
    assert "当前学习目标：Learn FastAPI" in output
