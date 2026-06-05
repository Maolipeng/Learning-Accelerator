# Learning Accelerator

**中文文档:** [README.zh-CN.md](README.zh-CN.md)

**English documentation:** [README.en.md](README.en.md)

Learning Accelerator is a reusable General Learning OS for agent runtimes. It combines prompt/skill instructions with a zero-dependency Python state store, CLI, structured practice records, review scheduling, concept progress, dashboard, and interactive TUI.

Learning Accelerator 是一个可复用的 General Learning OS：既可以作为 Agent Skill/Prompt 使用，也可以用本地 JSON 状态、CLI、结构化练习、概念进度、复习调度、dashboard 和交互式 TUI 管理连续学习过程。

## Quick Start

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json profile --domain technology --goal "Learn FastAPI"
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
```

## 快速开始

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json profile --domain technology --goal "学习 FastAPI"
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
```

## Documentation

| Topic | Chinese | English |
|---|---|---|
| README | [README.zh-CN.md](README.zh-CN.md) | [README.en.md](README.en.md) |
| Technical Architecture (canonical) | [docs/technical.md](docs/technical.md) | [docs/technical.md](docs/technical.md) |
| Technical Architecture | [docs/technical.zh-CN.md](docs/technical.zh-CN.md) | [docs/technical.en.md](docs/technical.en.md) |
| API | [docs/api.md](docs/api.md) | [docs/api.md](docs/api.md) |
| Extending | [docs/extending.md](docs/extending.md) | [docs/extending.md](docs/extending.md) |
| Install | [docs/install.md](docs/install.md) | [docs/install.md](docs/install.md) |
| Platforms | [docs/platforms.md](docs/platforms.md) | [docs/platforms.md](docs/platforms.md) |
| Release | [docs/release.md](docs/release.md) | [docs/release.md](docs/release.md) |
| JSON Schema | [schemas/learning_state.schema.json](schemas/learning_state.schema.json) | [schemas/learning_state.schema.json](schemas/learning_state.schema.json) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.md](CHANGELOG.md) |

## Core Capabilities

- Agent Skill and system prompt entry points.
- Local JSON persistence through `JsonStateStore`.
- Structured `ExerciseSpec` and `AttemptRecord`.
- Per-concept `ConceptProgress`.
- Spaced repetition and `review-priority`.
- Human-readable `dashboard`.
- Interactive standard-library `tui`.
- Machine-readable JSON schema.
- CI, release workflow, and version CLI.

## 核心能力

- Agent Skill 和 system prompt 入口。
- 基于 `JsonStateStore` 的本地 JSON 持久化。
- 结构化 `ExerciseSpec` 和 `AttemptRecord`。
- 概念级 `ConceptProgress`。
- 间隔复习和 `review-priority`。
- 可读的终端 `dashboard`。
- 标准库实现的交互式 `tui`。
- 机器可读 JSON Schema。
- CI、发布 workflow 和 `version` CLI。

## Useful Commands

```bash
python -m learning_accelerator.cli version
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
python -m learning_accelerator.cli --state-file .learning/state.json review-priority --limit 3
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
```

## 常用命令

```bash
python -m learning_accelerator.cli version
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
python -m learning_accelerator.cli --state-file .learning/state.json review-priority --limit 3
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
```
