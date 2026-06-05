# Learning Accelerator: General Learning OS

Learning Accelerator is a reusable dynamic learning skill and local learning-state system for agent runtimes. It is not only a teaching prompt. It combines learning state, review memory, spaced repetition, task-driven practice, structured `ExerciseSpec` records, `AttemptRecord` evaluation history, mistake diagnosis, difficulty adjustment, dashboard views, and an interactive terminal UI.

It can be used for technical learning such as Python, FastAPI, asyncio, MCP, RAG, WebGPU, Rust, Kubernetes, LangChain, and Pydantic. It can also be used for non-technical learning such as languages, writing, public speaking, exams, design, finance basics, and product management.

The user does not need prior programming knowledge. The agent should first ask about current skills, tools, goals, and constraints, then choose the right analogies, examples, practice format, and difficulty.

## What It Is

Learning Accelerator separates responsibilities:

- The LLM teaches, explains, generates exercises, evaluates answers, and diagnoses mistakes.
- The Python package persists state, manages deterministic review records, tracks concept progress, exposes CLI commands, and renders terminal views.
- The JSON state file keeps learning continuity across sessions and agent runtimes.

## Repository Map

```text
.
├── SKILL.md
├── SYSTEM_PROMPT.md
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── docs/
│   ├── api.md
│   ├── extending.md
│   ├── install.md
│   ├── platforms.md
│   ├── release.md
│   ├── technical.zh-CN.md
│   └── technical.en.md
├── learning_accelerator/
│   ├── state.py
│   ├── cli.py
│   ├── dashboard.py
│   └── tui.py
├── references/
│   └── learning_os_protocol.md
├── schemas/
│   └── learning_state.schema.json
├── examples/
└── tests/
```

## Install as a Skill

Codex:

```text
Use skill-installer to install the Learning-Accelerator skill from https://github.com/<owner>/Learning-Accelerator.
```

skills.sh:

```bash
npx skills find learning accelerator
npx skills add Maolipeng/Learning-Accelerator --skill learning-accelerator
```

Local development:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## CLI Quick Start

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json profile \
  --domain technology \
  --known-stack TypeScript React \
  --experience-level intermediate \
  --goal "Learn FastAPI dependency injection" \
  --outcome "Build a testable FastAPI API"
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
python -m learning_accelerator.cli --state-file .learning/state.json tui
```

## Structured Practice Flow

Create an exercise:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json exercise-generate \
  --topic "FastAPI dependency injection" \
  --concept "dependency injection" \
  --concept "Depends" \
  --difficulty normal \
  --task "Explain why Depends is not middleware." \
  --evaluation "Mentions per-request dependency resolution."
```

Record an attempt:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json attempt record "<exercise-id>" \
  --answer "Depends wraps every request like middleware." \
  --result partial \
  --score 45 \
  --mistake-type concept_confusion \
  --feedback "Confused dependency resolution with middleware execution." \
  --review-concept "dependency injection"
```

Inspect review and progress:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json review-priority --limit 3
python -m learning_accelerator.cli --state-file .learning/state.json concept-progress
python -m learning_accelerator.cli --state-file .learning/state.json prompt-context
```

## UI Commands

One-shot dashboard:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json dashboard
```

Interactive terminal UI:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json tui
```

The TUI supports dashboard, priority reviews, concept progress, due reviews, and adding tasks.

## Developer Documentation

- Technical architecture: [docs/technical.en.md](docs/technical.en.md)
- API: [docs/api.md](docs/api.md)
- Extending: [docs/extending.md](docs/extending.md)
- Release process: [docs/release.md](docs/release.md)
- State schema: [schemas/learning_state.schema.json](schemas/learning_state.schema.json)

## Verification

```bash
python -m pytest
git diff --check
python -m json.tool manifest.json >/dev/null
python -m json.tool schemas/learning_state.schema.json >/dev/null
```
