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
        ROOT / "SKILL.md",
        ROOT / "SYSTEM_PROMPT.md",
        ROOT / "README.md",
        ROOT / "manifest.json",
        ROOT / "agents" / "openai.yaml",
        ROOT / "references" / "learning_os_protocol.md",
        ROOT / "examples" / "python_function_example.md",
        ROOT / "examples" / "fastapi_example.md",
        ROOT / "examples" / "persistence_cli_example.md",
        ROOT / "examples" / "code_error_diagnosis_example.md",
        ROOT / "examples" / "project_learning_example.md",
        ROOT / "learning_accelerator" / "state.py",
        ROOT / "learning_accelerator" / "cli.py",
        ROOT / "pyproject.toml",
        ROOT / ".gitignore",
        ROOT / ".github" / "workflows" / "ci.yml",
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
        "Code Error Analysis",
        "Adaptive Difficulty",
    ])

    assert_contains(ROOT / "SYSTEM_PROMPT.md", [
        "语法",
        "类比",
        "实践",
        "最佳实践",
        "反模式",
        "回顾",
        "学习状态",
        "间隔重复",
        "代码错误诊断",
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
        "system-prompt based agents",
        "spaced repetition",
        "adaptive difficulty",
        "local JSON persistence",
        "CLI tooling",
        "CI workflow",
    ])

    assert_contains(ROOT / "references" / "learning_os_protocol.md", [
        "Learning State Schema",
        "Spaced Repetition",
        "Exercise Generation",
        "Code Error Analysis",
        "Difficulty Adjustment",
        "Project-Driven Learning",
        "Local JSON Persistence",
        "JsonStateStore",
    ])

    assert not (ROOT / ".DS_Store").exists(), ".DS_Store should not be packaged"
    assert "learning-agent-skill-prompt" not in read_text(ROOT / "README.md")

    print("Learning Accelerator Skill package structure is valid.")

if __name__ == "__main__":
    main()


def test_cli_and_coverage_configuration():
    assert_contains(ROOT / "pyproject.toml", [
        "learning-accelerator",
        "pytest",
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
        "本地持久化",
        "learning_accelerator.cli",
        "Learning-Accelerator",
        "python -m pip install -e .",
        "本地测试和覆盖率",
        ".github/workflows/ci.yml",
    ])


def test_skill_package_structure():
    main()
