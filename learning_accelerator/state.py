"""Persistent learning-state primitives for the Learning Accelerator skill.

The module intentionally uses only the Python standard library so the CLI can
run in constrained agent environments without dependency installation.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

DEFAULT_STATE: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "learner_profile": {
        "learning_domain": "general",
        "known_stack": [],
        "known_skills": [],
        "preferred_language": "zh-CN",
        "experience_level": "unknown",
        "learning_goal": "",
        "target_outcome": "",
        "target_project": "",
        "constraints": [],
    },
    "topic_state": {
        "current_topic": "",
        "level": "beginner",
        "mastered_concepts": [],
        "weak_concepts": [],
        "misconceptions": [],
        "open_questions": [],
    },
    "practice_state": {
        "completed_exercises": [],
        "failed_exercises": [],
        "current_tasks": [],
        "current_project_tasks": [],
        "last_code_errors": [],
    },
    "review_state": {
        "due_items": [],
        "review_history": [],
        "next_review_items": [],
    },
    "difficulty_state": {
        "current_difficulty": 1,
        "evidence": [],
        "next_adjustment": "same",
    },
}

REVIEW_INTERVALS_BY_RESULT = {
    "correct": 1,
    "second_correct": 3,
    "third_correct": 7,
    "incorrect": 0,
    "fuzzy": 0,
}

POSITIVE_DIFFICULTY_SIGNALS = {"exercise_completed", "explain_correct", "recall_correct"}
NEGATIVE_DIFFICULTY_SIGNALS = {"exercise_failed", "recall_incorrect", "explain_fuzzy", "setup_failed"}

DOMAIN_TEMPLATES: dict[str, dict[str, Any]] = {
    "general": {
        "domain": "general",
        "focus_areas": ["核心概念", "薄弱点", "练习", "复习"],
        "practice_types": ["解释复述", "小练习", "真实任务", "回顾问题"],
        "review_strategy": "Select 2-5 weak or recently learned items for spaced repetition.",
        "onboarding_questions": ["你想学习什么主题？", "你现在熟悉哪些技能、工具或相关经验？", "你希望达到什么具体结果？", "你每天或每周能投入多少时间？"],
    },
    "technology": {
        "domain": "technology",
        "focus_areas": ["概念", "语法/API", "工程实践", "调试", "测试"],
        "practice_types": ["代码", "小项目", "调试练习", "架构解释"],
        "review_strategy": "Review concepts, common mistakes, and project decisions.",
        "onboarding_questions": ["你想学哪门语言、框架、工具或架构？", "你现在熟悉哪些技术栈？", "你想做出什么可运行成果？", "你更想概念入门、项目实战还是错误诊断？"],
    },
    "language": {
        "domain": "language",
        "focus_areas": ["发音", "词汇", "句型", "听说读写", "文化语境"],
        "practice_types": ["跟读", "听写", "造句", "翻译", "小测"],
        "review_strategy": "Review weak vocabulary, sentence patterns, pronunciation, and recent mistakes.",
        "onboarding_questions": ["你想学习什么主题或哪门语言？", "你的目标是日常交流、考试、阅读还是写作？", "你现在熟悉哪些语言或发音体系？", "你每天能练多久？"],
    },
    "exam": {
        "domain": "exam",
        "focus_areas": ["考纲", "题型", "错题", "薄弱章节", "时间管理"],
        "practice_types": ["专项题", "模拟题", "错题复盘", "限时练习"],
        "review_strategy": "Review wrong answers, repeated weak chapters, and high-frequency exam patterns.",
        "onboarding_questions": ["你准备什么考试？", "考试日期或目标分数是什么？", "你目前最薄弱的题型或章节是什么？", "你每周能安排几次练习？"],
    },
    "writing": {
        "domain": "writing",
        "focus_areas": ["结构", "观点", "语言", "修改", "读者反馈"],
        "practice_types": ["短文", "改写", "提纲", "段落练习", "复盘"],
        "review_strategy": "Review repeated writing issues, structure patterns, and revised drafts.",
        "onboarding_questions": ["你想提升哪类写作？", "你现在常遇到的问题是什么？", "有没有目标读者或发表场景？", "你愿意每次写多少字？"],
    },
    "communication": {
        "domain": "communication",
        "focus_areas": ["结构化表达", "听众意识", "临场反应", "语速", "反馈"],
        "practice_types": ["60 秒表达", "录音复盘", "演讲提纲", "问答模拟"],
        "review_strategy": "Review structure, repeated hesitations, unclear points, and feedback notes.",
        "onboarding_questions": ["你想提升公开演讲、汇报、面试还是日常沟通？", "你最容易卡在哪一步？", "你是否愿意录音或写提纲复盘？", "你希望达到什么具体场景结果？"],
    },
}


class LearningStateError(ValueError):
    """Raised when persisted learning-state data is malformed."""


def today_iso() -> str:
    """Return today's date in ISO-8601 format."""

    return date.today().isoformat()


def _deep_merge(default: dict[str, Any], loaded: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(default)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _ensure_list(value: Any, field_name: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise LearningStateError(f"{field_name} must be a list")
    return value


def _stable_id(*parts: str) -> str:
    normalized = "\n".join(part.strip().lower() for part in parts)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]


def _upsert_by_id(items: list[dict[str, Any]], item: dict[str, Any]) -> list[dict[str, Any]]:
    for index, existing in enumerate(items):
        if existing.get("id") == item.get("id"):
            items[index] = {**existing, **item}
            return items
    items.append(item)
    return items


def create_review_item(
    concept: str,
    prompt: str,
    result: str = "correct",
    source: str = "manual",
    today: date | None = None,
) -> dict[str, Any]:
    """Create a review item using the default spaced-repetition intervals."""

    if result not in REVIEW_INTERVALS_BY_RESULT:
        allowed = ", ".join(sorted(REVIEW_INTERVALS_BY_RESULT))
        raise LearningStateError(f"result must be one of: {allowed}")
    base_day = today or date.today()
    due_day = base_day + timedelta(days=REVIEW_INTERVALS_BY_RESULT[result])
    return {
        "id": _stable_id("review", concept, prompt),
        "concept": concept,
        "prompt": prompt,
        "source": source,
        "result": result,
        "created_at": base_day.isoformat(),
        "due_at": due_day.isoformat(),
    }


@dataclass
class JsonStateStore:
    """Read and write Learning Accelerator state in a local JSON file."""

    path: Path

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()

    def load(self) -> dict[str, Any]:
        """Load state from disk, returning the default schema if absent."""

        if not self.path.exists():
            return copy.deepcopy(DEFAULT_STATE)
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LearningStateError(f"Invalid JSON in {self.path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise LearningStateError("Learning state root must be an object")
        return self.validate(self.migrate(_deep_merge(DEFAULT_STATE, raw)))

    def save(self, state: dict[str, Any]) -> dict[str, Any]:
        """Validate and persist state, creating parent directories as needed."""

        validated = self.validate(state)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return validated

    def reset(self) -> dict[str, Any]:
        """Overwrite the store with a fresh default state."""

        return self.save(copy.deepcopy(DEFAULT_STATE))

    def update_profile(
        self,
        *,
        learning_domain: str | None = None,
        known_stack: list[str] | None = None,
        known_skills: list[str] | None = None,
        preferred_language: str | None = None,
        experience_level: str | None = None,
        learning_goal: str | None = None,
        target_outcome: str | None = None,
        target_project: str | None = None,
        constraint: str | None = None,
    ) -> dict[str, Any]:
        """Update learner profile fields and persist the result."""

        state = self.load()
        profile = state["learner_profile"]
        if learning_domain:
            profile["learning_domain"] = learning_domain
        if known_stack is not None:
            profile["known_stack"] = known_stack
            if known_skills is None:
                profile["known_skills"] = known_stack
        if known_skills is not None:
            profile["known_skills"] = known_skills
        if preferred_language:
            profile["preferred_language"] = preferred_language
        if experience_level:
            if experience_level not in {"unknown", "no_programming", "beginner", "intermediate", "advanced"}:
                raise LearningStateError(
                    "experience_level must be unknown, no_programming, beginner, intermediate, or advanced"
                )
            profile["experience_level"] = experience_level
        if learning_goal is not None:
            profile["learning_goal"] = learning_goal
        if target_outcome is not None:
            profile["target_outcome"] = target_outcome
            profile["target_project"] = target_outcome
        if target_project is not None:
            profile["target_project"] = target_project
            if target_outcome is None:
                profile["target_outcome"] = target_project
        if constraint:
            constraints = _ensure_list(profile.get("constraints"), "constraints")
            if constraint not in constraints:
                constraints.append(constraint)
            profile["constraints"] = constraints
        return self.save(state)

    def add_task(self, name: str, notes: str = "") -> dict[str, Any]:
        """Add a current learning task, keeping legacy project task compatibility."""

        state = self.load()
        item = {
            "id": _stable_id("task", name),
            "name": name,
            "notes": notes,
            "status": "pending",
            "created_at": today_iso(),
        }
        tasks = _ensure_list(state["practice_state"].get("current_tasks"), "current_tasks")
        state["practice_state"]["current_tasks"] = _upsert_by_id(tasks, item)
        state["practice_state"]["current_project_tasks"] = [
            task["name"] for task in state["practice_state"]["current_tasks"]
        ]
        return self.save(state)

    def set_topic(self, topic: str, level: str | None = None) -> dict[str, Any]:
        """Set the active learning topic and optional level."""

        state = self.load()
        state["topic_state"]["current_topic"] = topic
        if level:
            state["topic_state"]["level"] = level
        return self.save(state)

    def record_concept(self, concept: str, status: str) -> dict[str, Any]:
        """Record a concept as mastered or weak, keeping lists de-duplicated."""

        if status not in {"mastered", "weak"}:
            raise LearningStateError("status must be 'mastered' or 'weak'")
        state = self.load()
        target_key = "mastered_concepts" if status == "mastered" else "weak_concepts"
        other_key = "weak_concepts" if status == "mastered" else "mastered_concepts"
        target = _ensure_list(state["topic_state"].get(target_key), target_key)
        other = _ensure_list(state["topic_state"].get(other_key), other_key)
        if concept not in target:
            target.append(concept)
        state["topic_state"][target_key] = target
        state["topic_state"][other_key] = [item for item in other if item != concept]
        return self.save(state)

    def add_review(
        self,
        concept: str,
        prompt: str,
        result: str = "correct",
        source: str = "manual",
    ) -> dict[str, Any]:
        """Add a scheduled review item and persist the state."""

        state = self.load()
        item = create_review_item(concept, prompt, result=result, source=source)
        next_items = _ensure_list(state["review_state"].get("next_review_items"), "next_review_items")
        next_items = _upsert_by_id(next_items, item)
        state["review_state"]["next_review_items"] = next_items
        return self.save(state)

    def complete_review(
        self,
        review_id: str,
        *,
        result: str,
        reschedule: bool = True,
        notes: str = "",
    ) -> dict[str, Any]:
        """Archive a review attempt and optionally schedule its next interval."""

        if result not in REVIEW_INTERVALS_BY_RESULT:
            allowed = ", ".join(sorted(REVIEW_INTERVALS_BY_RESULT))
            raise LearningStateError(f"result must be one of: {allowed}")

        state = self.load()
        review_state = state["review_state"]
        due_items = _ensure_list(review_state.get("due_items"), "due_items")
        next_items = _ensure_list(review_state.get("next_review_items"), "next_review_items")
        candidates = due_items + next_items
        matched = next((item for item in candidates if item.get("id") == review_id), None)
        if matched is None:
            raise LearningStateError(f"review item not found: {review_id}")

        review_state["due_items"] = [item for item in due_items if item.get("id") != review_id]
        review_state["next_review_items"] = [item for item in next_items if item.get("id") != review_id]

        completed = {
            **matched,
            "completed_result": result,
            "completed_at": today_iso(),
        }
        if notes:
            completed["notes"] = notes
        history = _ensure_list(review_state.get("review_history"), "review_history")
        history.append(completed)
        review_state["review_history"] = history

        if reschedule:
            review_state["next_review_items"] = _upsert_by_id(
                review_state["next_review_items"],
                create_review_item(
                    str(matched.get("concept", "")),
                    str(matched.get("prompt", "")),
                    result=result,
                    source=str(matched.get("source", "manual")),
                ),
            )
        self._apply_review_result_to_concepts(state, str(matched.get("concept", "")), result)
        self._record_evidence_in_state(state, "recall_correct" if result.startswith("correct") else "recall_incorrect", matched.get("prompt", ""))
        return self.save(state)

    def due_reviews(self, on_date: str | None = None) -> list[dict[str, Any]]:
        """Return review items whose due date is on or before ``on_date``."""

        target = on_date or today_iso()
        state = self.load()
        review_state = state["review_state"]
        candidates = []
        candidates.extend(_ensure_list(review_state.get("due_items"), "due_items"))
        candidates.extend(_ensure_list(review_state.get("next_review_items"), "next_review_items"))
        return [item for item in candidates if str(item.get("due_at", "")) <= target]

    def record_exercise(
        self,
        name: str,
        *,
        status: str,
        concepts: list[str] | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """Record a completed or failed exercise and update difficulty evidence."""

        if status not in {"completed", "failed"}:
            raise LearningStateError("status must be 'completed' or 'failed'")
        state = self.load()
        item = {
            "id": _stable_id("exercise", name),
            "name": name,
            "concepts": concepts or [],
            "notes": notes,
            "recorded_at": today_iso(),
        }
        key = "completed_exercises" if status == "completed" else "failed_exercises"
        exercises = _ensure_list(state["practice_state"].get(key), key)
        exercises = _upsert_by_id(exercises, item)
        state["practice_state"][key] = exercises
        signal = "exercise_completed" if status == "completed" else "exercise_failed"
        self._record_evidence_in_state(state, signal, notes or name)
        return self.save(state)

    def record_evidence(self, signal: str, detail: str = "", source: str = "manual") -> dict[str, Any]:
        """Record difficulty evidence and apply the current adjustment."""

        state = self.load()
        self._record_evidence_in_state(state, signal, detail, source=source)
        return self.save(state)

    def summary(self, on_date: str | None = None) -> dict[str, Any]:
        """Return a compact, agent-friendly learning-state summary."""

        state = self.load()
        profile = state["learner_profile"]
        topic = state["topic_state"]
        practice = state["practice_state"]
        difficulty = state["difficulty_state"]
        return {
            "learning_domain": profile.get("learning_domain", "general"),
            "known_skills": profile.get("known_skills", profile.get("known_stack", [])),
            "learning_goal": profile.get("learning_goal", ""),
            "target_outcome": profile.get("target_outcome", profile.get("target_project", "")),
            "target_project": profile.get("target_project", ""),
            "current_topic": topic.get("current_topic", ""),
            "level": topic.get("level", "beginner"),
            "mastered_concepts": topic.get("mastered_concepts", []),
            "weak_concepts": topic.get("weak_concepts", []),
            "due_reviews": self.due_reviews(on_date=on_date),
            "current_tasks": practice.get("current_tasks", []),
            "current_project_tasks": practice.get("current_project_tasks", []),
            "current_difficulty": difficulty.get("current_difficulty", 1),
            "next_adjustment": difficulty.get("next_adjustment", "same"),
        }

    def prompt_context(self, on_date: str | None = None) -> str:
        """Render summary data as concise prompt context for another agent."""

        summary = self.summary(on_date=on_date)
        due_concepts = [str(item.get("concept", "")) for item in summary["due_reviews"] if item.get("concept")]
        lines = [
            f"学习领域：{summary['learning_domain'] or 'general'}",
            f"已知技能：{', '.join(summary['known_skills']) if summary['known_skills'] else '未设置'}",
            f"当前学习目标：{summary['learning_goal'] or '未设置'}",
            f"当前主题：{summary['current_topic'] or '未设置'}",
            f"目标结果：{summary['target_outcome'] or '未设置'}",
            f"薄弱点：{', '.join(summary['weak_concepts']) if summary['weak_concepts'] else '无'}",
            f"今天需要复习：{', '.join(due_concepts) if due_concepts else '无'}",
            f"下一步任务：{', '.join(task['name'] for task in summary['current_tasks']) if summary['current_tasks'] else '未设置'}",
            f"当前难度：{summary['current_difficulty']}，下一步调整：{summary['next_adjustment']}",
        ]
        return "\n".join(lines)

    def onboarding_questions(self, domain: str | None = None) -> dict[str, Any]:
        """Return onboarding questions for a learning domain."""

        return self.domain_template(domain or "general")

    @staticmethod
    def domain_template(domain: str) -> dict[str, Any]:
        """Return a domain template, falling back to the general template."""

        return copy.deepcopy(DOMAIN_TEMPLATES.get(domain, DOMAIN_TEMPLATES["general"]))

    @staticmethod
    def migrate(state: dict[str, Any]) -> dict[str, Any]:
        """Apply lightweight in-memory migrations for older state files."""

        state["schema_version"] = SCHEMA_VERSION
        profile = state.get("learner_profile", {})
        if "known_skills" not in profile:
            profile["known_skills"] = list(profile.get("known_stack", []))
        if "learning_domain" not in profile:
            profile["learning_domain"] = "technology" if profile.get("known_stack") else "general"
        if not profile.get("target_outcome"):
            profile["target_outcome"] = profile.get("target_project", "")
        if not profile.get("target_project"):
            profile["target_project"] = profile.get("target_outcome", "")
        state["learner_profile"] = profile
        practice_state = state.get("practice_state", {})
        if not practice_state.get("current_tasks"):
            practice_state["current_tasks"] = [
                {
                    "id": _stable_id("task", str(task)),
                    "name": str(task),
                    "notes": "",
                    "status": "pending",
                    "created_at": today_iso(),
                }
                for task in _ensure_list(practice_state.get("current_project_tasks"), "current_project_tasks")
            ]
        if not practice_state.get("current_project_tasks"):
            practice_state["current_project_tasks"] = [
                str(task.get("name", "")) for task in _ensure_list(practice_state.get("current_tasks"), "current_tasks")
            ]
        state["practice_state"] = practice_state
        review_state = state.get("review_state", {})
        for key in ("due_items", "next_review_items", "review_history"):
            items = _ensure_list(review_state.get(key), key)
            for item in items:
                if isinstance(item, dict) and not item.get("id"):
                    item["id"] = _stable_id(
                        "review",
                        str(item.get("concept", "")),
                        str(item.get("prompt", "")),
                    )
            review_state[key] = items
        state["review_state"] = review_state
        return state

    @staticmethod
    def validate(state: dict[str, Any]) -> dict[str, Any]:
        """Validate the top-level schema and normalize missing keys."""

        if not isinstance(state, dict):
            raise LearningStateError("Learning state must be a dictionary")
        normalized = _deep_merge(DEFAULT_STATE, state)
        normalized = JsonStateStore.migrate(normalized)
        if normalized.get("schema_version") != SCHEMA_VERSION:
            raise LearningStateError(f"schema_version must be {SCHEMA_VERSION}")
        for section in DEFAULT_STATE:
            if section == "schema_version":
                continue
            if section not in normalized or not isinstance(normalized[section], dict):
                raise LearningStateError(f"{section} must be an object")
        topic = normalized["topic_state"]
        if topic.get("level") not in {"beginner", "intermediate", "advanced"}:
            raise LearningStateError("topic_state.level must be beginner, intermediate, or advanced")
        difficulty = normalized["difficulty_state"].get("current_difficulty")
        if not isinstance(difficulty, int) or not 1 <= difficulty <= 5:
            raise LearningStateError("difficulty_state.current_difficulty must be an integer from 1 to 5")
        return normalized

    @staticmethod
    def _apply_review_result_to_concepts(state: dict[str, Any], concept: str, result: str) -> None:
        if not concept:
            return
        topic = state["topic_state"]
        weak = _ensure_list(topic.get("weak_concepts"), "weak_concepts")
        mastered = _ensure_list(topic.get("mastered_concepts"), "mastered_concepts")
        if result in {"incorrect", "fuzzy"}:
            if concept not in weak:
                weak.append(concept)
            mastered = [item for item in mastered if item != concept]
        elif result in {"second_correct", "third_correct"}:
            if concept not in mastered:
                mastered.append(concept)
            weak = [item for item in weak if item != concept]
        topic["weak_concepts"] = weak
        topic["mastered_concepts"] = mastered

    @staticmethod
    def _record_evidence_in_state(
        state: dict[str, Any],
        signal: str,
        detail: Any = "",
        *,
        source: str = "manual",
    ) -> None:
        difficulty = state["difficulty_state"]
        evidence = _ensure_list(difficulty.get("evidence"), "difficulty_state.evidence")
        evidence.append({
            "signal": signal,
            "detail": str(detail),
            "source": source,
            "recorded_at": today_iso(),
        })
        difficulty["evidence"] = evidence[-20:]
        JsonStateStore._adjust_difficulty_in_state(state)

    @staticmethod
    def _adjust_difficulty_in_state(state: dict[str, Any]) -> None:
        difficulty = state["difficulty_state"]
        evidence = _ensure_list(difficulty.get("evidence"), "difficulty_state.evidence")
        recent = evidence[-2:]
        positive = sum(1 for item in recent if item.get("signal") in POSITIVE_DIFFICULTY_SIGNALS)
        negative = sum(1 for item in recent if item.get("signal") in NEGATIVE_DIFFICULTY_SIGNALS)
        current = difficulty.get("current_difficulty", 1)
        if positive >= 2:
            difficulty["next_adjustment"] = "harder"
            difficulty["current_difficulty"] = min(5, current + 1)
        elif negative >= 2:
            difficulty["next_adjustment"] = "easier"
            difficulty["current_difficulty"] = max(1, current - 1)
        else:
            difficulty["next_adjustment"] = "same"
            difficulty["current_difficulty"] = current
