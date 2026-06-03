"""Command-line interface for Learning Accelerator JSON persistence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .state import JsonStateStore

DEFAULT_STATE_PATH = Path.home() / ".learning-accelerator" / "state.json"


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="learning-accelerator",
        description="Persist and inspect AI Learning OS learning state.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_PATH),
        help="Path to the JSON state file. Defaults to ~/.learning-accelerator/state.json.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create or overwrite a state file with the default schema.")
    subparsers.add_parser("show", help="Print the full learning state as JSON.")

    profile = subparsers.add_parser("profile", help="Update learner profile fields.")
    profile.add_argument("--known-stack", nargs="*", help="Known technologies, e.g. JS TS React.")
    profile.add_argument("--language", help="Preferred response language, e.g. zh-CN or en-US.")
    profile.add_argument("--goal", help="Learning goal.")
    profile.add_argument("--project", help="Target project.")
    profile.add_argument("--constraint", help="Add one learning constraint.")

    topic = subparsers.add_parser("topic", help="Set current topic and optional level.")
    topic.add_argument("name", help="Topic name, e.g. FastAPI dependency injection.")
    topic.add_argument("--level", choices=["beginner", "intermediate", "advanced"])

    concept = subparsers.add_parser("concept", help="Record a mastered or weak concept.")
    concept.add_argument("status", choices=["mastered", "weak"])
    concept.add_argument("name", help="Concept name.")

    review = subparsers.add_parser("review", help="Schedule a review prompt.")
    review.add_argument("concept", help="Concept to review.")
    review.add_argument("prompt", help="Recall prompt.")
    review.add_argument(
        "--result",
        default="correct",
        choices=["correct", "second_correct", "third_correct", "incorrect", "fuzzy"],
        help="Latest recall result used to calculate the next due date.",
    )
    review.add_argument("--source", default="manual", help="Source of the review item.")

    due = subparsers.add_parser("due", help="Print review items due by a date.")
    due.add_argument("--date", help="ISO date, defaults to today.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = JsonStateStore(args.state_file)

    if args.command == "init":
        _print_json(store.reset())
    elif args.command == "show":
        _print_json(store.load())
    elif args.command == "profile":
        _print_json(
            store.update_profile(
                known_stack=args.known_stack,
                preferred_language=args.language,
                learning_goal=args.goal,
                target_project=args.project,
                constraint=args.constraint,
            )
        )
    elif args.command == "topic":
        _print_json(store.set_topic(args.name, level=args.level))
    elif args.command == "concept":
        _print_json(store.record_concept(args.name, args.status))
    elif args.command == "review":
        _print_json(store.add_review(args.concept, args.prompt, result=args.result, source=args.source))
    elif args.command == "due":
        _print_json(store.due_reviews(on_date=args.date))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
