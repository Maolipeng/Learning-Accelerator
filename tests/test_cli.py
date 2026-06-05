from __future__ import annotations

import json

from learning_accelerator.cli import main


def test_cli_version_prints_package_and_schema_version(capsys):
    assert main(["version"]) == 0

    version = json.loads(capsys.readouterr().out)
    assert version["name"] == "learning-accelerator"
    assert version["version"] == "1.6.0"
    assert version["schema_version"] == 1


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


def test_cli_onboarding_task_and_domain_template(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main(["--state-file", str(state_file), "onboarding", "--domain", "language"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "profile",
        "--domain",
        "language",
        "--goal",
        "通过日语 N5",
        "--outcome",
        "能读写基础假名",
    ]) == 0
    assert main(["--state-file", str(state_file), "task", "add", "每天复习 5 个假名"]) == 0
    assert main(["--state-file", str(state_file), "domain-template", "language"]) == 0
    assert main(["--state-file", str(state_file), "prompt-context"]) == 0

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["learner_profile"]["target_outcome"] == "能读写基础假名"
    assert state["practice_state"]["current_tasks"][0]["name"] == "每天复习 5 个假名"

    output = capsys.readouterr().out
    assert "你想学习什么主题" in output
    assert '"domain": "language"' in output
    assert "目标结果：能读写基础假名" in output


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


def test_cli_structured_exercise_and_attempt_flow(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "exercise-generate",
        "--topic",
        "FastAPI dependencies",
        "--concept",
        "dependency injection",
        "--concept",
        "Depends",
        "--difficulty",
        "normal",
        "--task",
        "Build a route that injects a repository dependency.",
        "--expected-output",
        "GET /items returns JSON from the injected repository.",
        "--constraint",
        "Use Depends",
        "--evaluation",
        "Route uses dependency injection",
        "--hint",
        "Start by writing a provider function.",
    ]) == 0

    state = json.loads(state_file.read_text(encoding="utf-8"))
    exercise_id = state["practice_state"]["exercise_specs"][0]["id"]

    assert main(["--state-file", str(state_file), "exercise-show", exercise_id]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "attempt",
        "record",
        exercise_id,
        "--answer",
        "Depends wraps every request like middleware.",
        "--result",
        "partial",
        "--score",
        "45",
        "--mistake-type",
        "concept_confusion",
        "--feedback",
        "Confused dependency resolution with middleware execution.",
        "--review-concept",
        "dependency injection",
    ]) == 0

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["practice_state"]["exercise_specs"][0]["difficulty"] == "normal"
    assert state["practice_state"]["attempt_records"][0]["exercise_id"] == exercise_id
    assert state["review_state"]["next_review_items"][0]["concept"] == "dependency injection"

    output = capsys.readouterr().out
    assert '"task": "Build a route that injects a repository dependency."' in output
    assert '"mistake_type": "concept_confusion"' in output


def test_cli_concept_progress_and_review_priority(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
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
    ]) == 0
    assert main(["--state-file", str(state_file), "concept-progress"]) == 0
    assert main(["--state-file", str(state_file), "review-priority", "--date", "2999-01-01", "--limit", "1"]) == 0

    output = capsys.readouterr().out
    assert '"dependency injection"' in output
    assert '"correct_streak": 1' in output
    assert '"priority"' in output


def test_cli_dashboard_outputs_human_readable_state(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main(["--state-file", str(state_file), "profile", "--goal", "Learn FastAPI", "--outcome", "Build a RAG API"]) == 0
    assert main(["--state-file", str(state_file), "topic", "dependency injection", "--level", "beginner"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "review",
        "Depends",
        "Explain Depends.",
        "--result",
        "incorrect",
    ]) == 0
    assert main(["--state-file", str(state_file), "dashboard", "--date", "2999-01-01"]) == 0

    output = capsys.readouterr().out
    assert "Learning Accelerator Dashboard" in output
    assert "Goal: Learn FastAPI" in output
    assert "Outcome: Build a RAG API" in output
    assert "Topic: dependency injection (beginner)" in output
    assert "Depends" in output
