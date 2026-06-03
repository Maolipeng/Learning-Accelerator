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
    summary = subparsers.add_parser("summary", help="Print a compact learning-state summary as JSON.")
    summary.add_argument("--date", help="ISO date for due review filtering, defaults to today.")
    prompt_context = subparsers.add_parser("prompt-context", help="Print concise prompt context for another agent.")
    prompt_context.add_argument("--date", help="ISO date for due review filtering, defaults to today.")

    profile = subparsers.add_parser("profile", help="Update learner profile fields.")
    profile.add_argument("--known-stack", nargs="*", help="Known technologies, e.g. JS TS React.")
    profile.add_argument("--language", help="Preferred response language, e.g. zh-CN or en-US.")
    profile.add_argument(
        "--experience-level",
        choices=["unknown", "no_programming", "beginner", "intermediate", "advanced"],
        help="Learner experience level.",
    )
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

    review_complete = subparsers.add_parser("review-complete", help="Complete and archive a review item.")
    review_complete.add_argument("review_id", help="Review item id.")
    review_complete.add_argument(
        "--result",
        required=True,
        choices=["correct", "second_correct", "third_correct", "incorrect", "fuzzy"],
        help="Recall result used for history and optional rescheduling.",
    )
    review_complete.add_argument("--notes", default="", help="Optional completion notes.")
    review_complete.add_argument(
        "--no-reschedule",
        action="store_true",
        help="Archive the review without scheduling the next interval.",
    )

    due = subparsers.add_parser("due", help="Print review items due by a date.")
    due.add_argument("--date", help="ISO date, defaults to today.")

    exercise = subparsers.add_parser("exercise", help="Record a completed or failed exercise.")
    exercise.add_argument("status", choices=["complete", "fail"])
    exercise.add_argument("name", help="Exercise name.")
    exercise.add_argument("--concept", action="append", default=[], help="Concept covered by this exercise.")
    exercise.add_argument("--notes", default="", help="Optional exercise notes.")

    evidence = subparsers.add_parser("evidence", help="Record difficulty-adjustment evidence.")
    evidence.add_argument("signal", help="Evidence signal, e.g. exercise_completed or recall_incorrect.")
    evidence.add_argument("detail", nargs="?", default="", help="Evidence detail.")
    evidence.add_argument("--source", default="manual", help="Evidence source.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = JsonStateStore(args.state_file)

    if args.command == "init":
        _print_json(store.reset())
    elif args.command == "show":
        _print_json(store.load())
    elif args.command == "summary":
        _print_json(store.summary(on_date=args.date))
    elif args.command == "prompt-context":
        print(store.prompt_context(on_date=args.date))
    elif args.command == "profile":
        _print_json(
            store.update_profile(
                known_stack=args.known_stack,
                preferred_language=args.language,
                experience_level=args.experience_level,
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
    elif args.command == "review-complete":
        _print_json(
            store.complete_review(
                args.review_id,
                result=args.result,
                reschedule=not args.no_reschedule,
                notes=args.notes,
            )
        )
    elif args.command == "due":
        _print_json(store.due_reviews(on_date=args.date))
    elif args.command == "exercise":
        status = "completed" if args.status == "complete" else "failed"
        _print_json(store.record_exercise(args.name, status=status, concepts=args.concept, notes=args.notes))
    elif args.command == "evidence":
        _print_json(store.record_evidence(args.signal, args.detail, source=args.source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
