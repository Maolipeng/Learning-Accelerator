import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_contains(path: Path, keywords: list[str]):
    text = path.read_text(encoding="utf-8")
    missing = [kw for kw in keywords if kw not in text]
    assert not missing, f"{path.name} missing keywords: {missing}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_skill_frontmatter():
    text = read_text(ROOT / "SKILL.md")
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---", 4)
    assert end != -1, "SKILL.md frontmatter must be closed"
    frontmatter = text[4:end]
    assert "name: learning-accelerator" in frontmatter
    assert "description:" in frontmatter
    assert "dynamic learning agent" in frontmatter or "AI Learning OS" in frontmatter


def main():
    required_files = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "GEMINI.md",
        ROOT / "SKILL.md",
        ROOT / "SYSTEM_PROMPT.md",
        ROOT / ".cursor" / "rules" / "learning-accelerator.mdc",
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "README.en.md",
        ROOT / "manifest.json",
        ROOT / "skills.sh.json",
        ROOT / "agents" / "openai.yaml",
        ROOT / "docs" / "community-article.md",
        ROOT / "docs" / "api.md",
        ROOT / "docs" / "extending.md",
        ROOT / "docs" / "install.md",
        ROOT / "docs" / "platforms.md",
        ROOT / "docs" / "release.md",
        ROOT / "docs" / "technical.md",
        ROOT / "docs" / "technical.zh-CN.md",
        ROOT / "docs" / "technical.en.md",
        ROOT / "schemas" / "learning_state.schema.json",
        ROOT / "CHANGELOG.md",
        ROOT / "references" / "learning_os_protocol.md",
        ROOT / "examples" / "no_prior_programming_example.md",
        ROOT / "examples" / "language_learning_example.md",
        ROOT / "examples" / "non_technical_learning_example.md",
        ROOT / "examples" / "python_function_example.md",
        ROOT / "examples" / "fastapi_example.md",
        ROOT / "examples" / "persistence_cli_example.md",
        ROOT / "examples" / "code_error_diagnosis_example.md",
        ROOT / "examples" / "project_learning_example.md",
        ROOT / "learning_accelerator" / "state.py",
        ROOT / "learning_accelerator" / "cli.py",
        ROOT / "learning_accelerator" / "dashboard.py",
        ROOT / "learning_accelerator" / "tui.py",
        ROOT / "pyproject.toml",
        ROOT / ".gitignore",
        ROOT / ".github" / "workflows" / "ci.yml",
        ROOT / ".github" / "workflows" / "release.yml",
    ]

    for file in required_files:
        assert file.exists(), f"Missing file: {file}"

    assert_skill_frontmatter()

    assert_contains(ROOT / "SKILL.md", [
        "Cognitive Positioning",
        "Prior Knowledge Mapping",
        "Minimal Runnable Example",
        "Best Practices",
        "Anti-patterns",
        "Progressive Recall",
        "Review Memory",
        "Spaced Repetition",
        "Task-Driven Practice",
        "analyze mistakes",
        "Adaptive Difficulty",
        "No-Prior-Programming Mapping",
        "Do not assume frontend knowledge",
        "list their current skills",
    ])

    assert_contains(ROOT / "SYSTEM_PROMPT.md", [
        "基础表达",
        "类比",
        "实践",
        "最佳实践",
        "反模式",
        "回顾",
        "学习状态",
        "间隔重复",
        "错误诊断",
        "技术学习只是一个领域",
        "不要默认用户懂前端",
        "小白",
        "列出现有技能",
    ])

    assert_contains(ROOT / "agents" / "openai.yaml", [
        "display_name",
        "short_description",
        "allow_implicit_invocation",
        "$learning-accelerator",
    ])

    assert_contains(ROOT / "manifest.json", [
        "compatible_with",
        "Codex skills",
        "Claude Code skills",
        "Cursor rules",
        "Gemini CLI project guides",
        "AGENTS.md-compatible coding agents",
        "system-prompt based agents",
        "spaced repetition",
        "adaptive difficulty",
        "review completion and archival",
        "prompt-context export",
        "local JSON persistence",
        "CLI tooling",
        "CI workflow",
        "no-prior-programming learner",
        "language learner",
        "communication learner",
        "skill-installer",
        "skills_sh",
        "as_skills_sh",
        "npx skills find",
        "npx skills add",
        "skills_sh_page_config",
        "distribution",
        "codex_skill_installer",
        "github_source",
        "as_codex_local_dev",
        "schemas/learning_state.schema.json",
        "docs/api.md",
        "docs/extending.md",
        "CHANGELOG.md",
        "docs/release.md",
        "docs/technical.md",
        "README.zh-CN.md",
        "README.en.md",
        "docs/technical.zh-CN.md",
        "docs/technical.en.md",
    ])

    assert_contains(ROOT / "skills.sh.json", [
        "https://skills.sh/schemas/skills.sh.schema.json",
        "Learning",
        "learning-accelerator",
        "spaced repetition",
    ])

    assert_contains(ROOT / "references" / "learning_os_protocol.md", [
        "Learning State Schema",
        "Spaced Repetition",
        "Exercise Generation",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "Error Analysis",
        "Difficulty Adjustment",
        "exercise-generate",
        "exercise-show",
        "attempt record",
        "concept-progress",
        "review-priority",
        "dashboard",
        "tui",
        "review-complete",
        "prompt-context",
        "Task-Driven Learning",
        "Local JSON Persistence",
        "JsonStateStore",
        "experience_level",
        "learning_domain",
        "known_skills",
        "target_outcome",
        "current_tasks",
        "onboarding --domain",
        "domain-template",
        "task add",
    ])

    assert_contains(ROOT / "examples" / "no_prior_programming_example.md", [
        "零编程基础",
        "函数可以理解成",
        "有名字的一组步骤",
        "return",
        "状态更新",
    ])

    assert_contains(ROOT / "examples" / "language_learning_example.md", [
        "日语",
        "language",
        "中文拼音",
        "五个基础平假名",
        "状态更新",
    ])

    assert_contains(ROOT / "examples" / "non_technical_learning_example.md", [
        "公开演讲",
        "communication",
        "结构化表达",
        "评价标准",
        "状态更新",
    ])

    assert_contains(ROOT / "AGENTS.md", [
        "SKILL.md",
        "SYSTEM_PROMPT.md",
        "learning_os_protocol.md",
        "learning_accelerator.cli",
        "Claude Code",
    ])

    assert_contains(ROOT / "CLAUDE.md", [
        "Claude Code",
        "SKILL.md",
        "SYSTEM_PROMPT.md",
        "learning_os_protocol.md",
        "learning_accelerator.cli",
        "~/.claude/skills/learning-accelerator",
    ])

    assert_contains(ROOT / "GEMINI.md", [
        "Gemini CLI",
        "SYSTEM_PROMPT.md",
        "learning_os_protocol.md",
        "learning_accelerator.cli",
        ".learning/state.json",
    ])

    assert_contains(ROOT / ".cursor" / "rules" / "learning-accelerator.mdc", [
        "alwaysApply: false",
        "SKILL.md",
        "SYSTEM_PROMPT.md",
        "learning_os_protocol.md",
        "learning_accelerator.cli",
    ])

    assert_contains(ROOT / "docs" / "platforms.md", [
        "Codex",
        "Claude Code",
        "Cursor",
        "Gemini CLI",
        "AGENTS.md",
        "SYSTEM_PROMPT.md",
    ])

    assert_contains(ROOT / "docs" / "community-article.md", [
        "General Learning OS",
        "整体架构",
        "```mermaid",
        "Agent 工作流",
        "状态流转图",
        "难度调整逻辑",
        "多平台适配",
        "安装和分发",
        "和已有学习类 Skill 的区别",
        "self-learning",
        "continuous-learning",
        "coding tutor",
        "一个真实回答过程会是什么样",
        "函数定义格式",
        "npx skills add Maolipeng/Learning-Accelerator --skill learning-accelerator",
        "prompt-context",
        "review-complete",
        "exercise-generate",
        "attempt record",
    ])

    assert_contains(ROOT / "docs" / "install.md", [
        "Install From GitHub In Codex",
        "skills.sh",
        "npx skills find learning accelerator",
        "npx skills add Maolipeng/Learning-Accelerator --skill learning-accelerator",
        "skills.sh Publication Checklist",
        "skills.sh.json",
        "anonymous telemetry",
        "Codex `skill-installer` and `npx skills` are complementary",
        "skill-installer",
        "Restart Codex",
        "Local Development Install",
        "~/.codex/skills/learning-accelerator",
        "Python CLI",
    ])

    assert_contains(ROOT / "docs" / "api.md", [
        "JsonStateStore",
        "create_review_item",
        "create_exercise_spec",
        "record_attempt",
        "priority_reviews",
        "concept_progress",
        "CLI Commands",
        "dashboard",
        "tui",
        "version",
        "Error Handling",
    ])

    assert_contains(ROOT / "docs" / "extending.md", [
        "Extension Points",
        "DOMAIN_TEMPLATES",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "Review Strategy",
        "Do Not Break",
    ])

    assert_contains(ROOT / "CHANGELOG.md", [
        "# Changelog",
        "Unreleased",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "dashboard",
        "tui",
        "v1.6.0",
        "v1.2.0",
    ])

    assert_contains(ROOT / "docs" / "release.md", [
        "Release Checklist",
        "version",
        "CHANGELOG.md",
        "git tag",
        "python -m pytest",
        "release.yml",
        "artifact",
    ])

    assert_contains(ROOT / "docs" / "technical.md", [
        "Technical Architecture",
        "System Boundary",
        "Module Map",
        "State Flow",
        "Learning State Model",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "Review Priority",
        "CLI Surface",
        "Testing Strategy",
        "Release Boundary",
    ])

    assert_contains(ROOT / "docs" / "technical.zh-CN.md", [
        "技术架构",
        "系统边界",
        "模块地图",
        "状态流",
        "学习状态模型",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "复习优先级",
        "CLI 表面",
        "测试策略",
        "发布边界",
    ])

    assert_contains(ROOT / "docs" / "technical.en.md", [
        "Technical Architecture",
        "System Boundary",
        "Module Map",
        "State Flow",
        "Learning State Model",
        "ExerciseSpec",
        "AttemptRecord",
        "ConceptProgress",
        "Review Priority",
        "CLI Surface",
        "Testing Strategy",
        "Release Boundary",
    ])

    assert_contains(ROOT / ".github" / "workflows" / "release.yml", [
        "Release",
        "on:",
        "tags:",
        "v*",
        "python -m pytest",
        "python -m build",
        "actions/upload-artifact",
    ])

    schema = json.loads(read_text(ROOT / "schemas" / "learning_state.schema.json"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["title"] == "Learning Accelerator State"
    assert schema["properties"]["schema_version"]["const"] == 1
    assert "learner_profile" in schema["required"]
    assert "topic_state" in schema["required"]
    assert "practice_state" in schema["required"]
    assert "review_state" in schema["required"]
    assert "difficulty_state" in schema["required"]
    assert "concept_progress" in schema["properties"]["topic_state"]["properties"]
    assert "exercise_specs" in schema["properties"]["practice_state"]["properties"]
    assert "attempt_records" in schema["properties"]["practice_state"]["properties"]

    assert not (ROOT / ".DS_Store").exists(), ".DS_Store should not be packaged"
    assert "learning-agent-skill-prompt" not in read_text(ROOT / "README.md")

    print("Learning Accelerator Skill package structure is valid.")

if __name__ == "__main__":
    main()


def test_cli_and_coverage_configuration():
    assert_contains(ROOT / "pyproject.toml", [
        "learning-accelerator",
        "pytest",
        "pytest-cov",
        "optional-dependencies",
        "tool.setuptools.packages.find",
        "learning_accelerator*",
        "fail_under",
    ])
    assert_contains(ROOT / ".gitignore", [
        "__pycache__/",
        "coverage.xml",
        ".learning/",
    ])
    assert_contains(ROOT / ".github" / "workflows" / "ci.yml", [
        "python -m pytest",
        "--cov=learning_accelerator",
        "coverage.xml",
        "pytest-cov",
        "actions/upload-artifact",
    ])
    assert_contains(ROOT / "README.md", [
        "learning_accelerator.cli",
        "中文文档",
        "English documentation",
        "README.zh-CN.md",
        "README.en.md",
        "prompt-context",
        "dashboard",
        "tui",
        "General Learning OS",
        "docs/api.md",
        "docs/extending.md",
        "schemas/learning_state.schema.json",
        "CHANGELOG.md",
        "docs/release.md",
        "docs/technical.md",
        "docs/technical.zh-CN.md",
        "docs/technical.en.md",
        "version",
    ])

    assert_contains(ROOT / "README.zh-CN.md", [
        "本地持久化",
        "Learning-Accelerator",
        "review-complete",
        "一轮真实学习落盘流程",
        "零编程基础入门",
        "日语学习",
        "非技术学习",
        "skill-installer",
        "skills.sh",
        "npx skills find learning accelerator",
        "npx skills add Maolipeng/Learning-Accelerator --skill learning-accelerator",
        "docs/install.md",
        "安装后重启 Codex",
        "不要求用户预先懂前端或编程",
        "--experience-level no_programming",
        "--domain language",
        "--known-skill",
        "onboarding --domain language",
        "domain-template language",
        "task add",
        "先问我目前熟悉哪些技能或工具",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".cursor/rules/learning-accelerator.mdc",
        "docs/platforms.md",
        "~/.claude/skills/learning-accelerator",
        "python -m pip install -e \".[dev]\"",
        "python -m pip install --upgrade pip",
        "python -m pip install -e .",
        "本地测试和覆盖率",
        ".github/workflows/ci.yml",
    ])

    assert_contains(ROOT / "README.en.md", [
        "Learning Accelerator",
        "General Learning OS",
        "What It Is",
        "Repository Map",
        "Install as a Skill",
        "CLI Quick Start",
        "Structured Practice Flow",
        "ExerciseSpec",
        "AttemptRecord",
        "review-priority",
        "concept-progress",
        "dashboard",
        "tui",
        "Developer Documentation",
        "docs/technical.en.md",
        "schemas/learning_state.schema.json",
        "python -m pytest",
    ])

    assert_contains(ROOT / "learning_accelerator" / "dashboard.py", [
        "render_dashboard",
        "Learning Accelerator Dashboard",
        "Priority Reviews",
        "Concept Progress",
        "Current Tasks",
    ])

    assert_contains(ROOT / "learning_accelerator" / "tui.py", [
        "run_tui",
        "Learning Accelerator TUI",
        "Priority Reviews",
        "Concept Progress",
        "Add Task",
    ])


def test_skill_package_structure():
    main()
