"""Interactive terminal UI for Learning Accelerator."""

from __future__ import annotations

import sys
from typing import Callable, TextIO

from .dashboard import render_dashboard
from .state import JsonStateStore

InputFunc = Callable[[str], str]


MENU = """Learning Accelerator TUI
========================
1. Dashboard
2. Priority Reviews
3. Concept Progress
4. Due Reviews
5. Add Task
q. Quit
"""


def _write(output: TextIO, text: str = "") -> None:
    output.write(text + "\n")


def _write_jsonish_list(output: TextIO, title: str, items: list[dict]) -> None:
    _write(output, title)
    _write(output, "-" * len(title))
    if not items:
        _write(output, "None.")
        return
    for item in items:
        concept = item.get("concept", item.get("name", "unknown"))
        detail = item.get("prompt", item.get("status", ""))
        if "priority" in item:
            _write(output, f"{concept} | priority {item.get('priority')} | due {item.get('due_at')}")
        elif detail:
            _write(output, f"{concept} | {detail}")
        else:
            _write(output, str(concept))


def _write_concept_progress(output: TextIO, progress: dict) -> None:
    _write(output, "Concept Progress")
    _write(output, "----------------")
    if not progress:
        _write(output, "No concept progress yet.")
        return
    for concept in sorted(progress):
        item = progress[concept]
        _write(
            output,
            f"{concept} | strength {item.get('strength', 'unknown')} | "
            f"attempts {item.get('attempts', 0)} | streak {item.get('correct_streak', 0)} | "
            f"failures {item.get('failure_count', 0)} | next {item.get('next_due_at', 'unset')}",
        )


def run_tui(
    store: JsonStateStore,
    *,
    input_func: InputFunc = input,
    output: TextIO | None = None,
    on_date: str | None = None,
) -> int:
    """Run the interactive terminal UI command loop."""

    out = output or sys.stdout
    while True:
        _write(out, MENU.rstrip())
        choice = input_func("Choose: ").strip()

        if choice.lower() in {"q", "quit", "exit"}:
            _write(out, "Goodbye.")
            return 0
        if choice == "1":
            _write(out, render_dashboard(store.summary(on_date=on_date)).rstrip())
        elif choice == "2":
            _write_jsonish_list(out, "Priority Reviews", store.priority_reviews(on_date=on_date))
        elif choice == "3":
            _write_concept_progress(out, store.load()["topic_state"].get("concept_progress", {}))
        elif choice == "4":
            _write_jsonish_list(out, "Due Reviews", store.due_reviews(on_date=on_date))
        elif choice == "5":
            name = input_func("Task name: ").strip()
            if not name:
                _write(out, "Task name is required.")
            else:
                store.add_task(name)
                _write(out, f"Task added: {name}")
        else:
            _write(out, f"Unknown choice: {choice}")
