from __future__ import annotations

from io import StringIO

from learning_accelerator.state import JsonStateStore
from learning_accelerator.tui import run_tui


def scripted_input(values: list[str]):
    iterator = iter(values)

    def _input(prompt: str = "") -> str:
        return next(iterator)

    return _input


def test_tui_renders_dashboard_and_quits(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    store.update_profile(learning_goal="Learn FastAPI", target_outcome="Build a RAG API")
    store.set_topic("dependency injection", level="beginner")

    output = StringIO()
    result = run_tui(store, input_func=scripted_input(["1", "q"]), output=output, on_date="2999-01-01")

    text = output.getvalue()
    assert result == 0
    assert "Learning Accelerator TUI" in text
    assert "1. Dashboard" in text
    assert "Learning Accelerator Dashboard" in text
    assert "Goal: Learn FastAPI" in text
    assert "Goodbye." in text


def test_tui_lists_priority_reviews_and_adds_task(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    store.add_review("Depends", "Explain Depends.", result="incorrect")

    output = StringIO()
    result = run_tui(
        store,
        input_func=scripted_input(["2", "5", "Implement one route", "q"]),
        output=output,
        on_date="2999-01-01",
    )

    state = store.load()
    text = output.getvalue()
    assert result == 0
    assert "Priority Reviews" in text
    assert "Depends | priority" in text
    assert "Task added: Implement one route" in text
    assert state["practice_state"]["current_tasks"][0]["name"] == "Implement one route"


def test_tui_handles_unknown_choice(tmp_path):
    store = JsonStateStore(tmp_path / "state.json")
    output = StringIO()

    run_tui(store, input_func=scripted_input(["unknown", "q"]), output=output)

    assert "Unknown choice: unknown" in output.getvalue()
