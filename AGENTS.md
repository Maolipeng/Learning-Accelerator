# Learning Accelerator Agent Guide

This repository packages a reusable AI Learning OS for coding agents and general assistant runtimes.

## What To Load

- `SKILL.md`: canonical skill entry for agents that support markdown skills.
- `SYSTEM_PROMPT.md`: fallback for agents that only support system or developer instructions.
- `references/learning_os_protocol.md`: state schema and operating protocol for memory, review, practice, debugging, and difficulty adjustment.
- `examples/`: concrete output examples for concept learning, project learning, CLI persistence, and code-error diagnosis.
- `learning_accelerator/`: optional Python JSON state store and CLI.

## Agent Behavior

When the user asks to learn, review, practice, debug learning code, generate exercises, or adjust difficulty:

1. Read existing learning state if a host memory, `.learning/state.json`, or `~/.learning-accelerator/state.json` exists.
2. During onboarding, ask the learner to list current skills, familiar tools, and comfort level; "no prior programming" is a valid answer.
3. Choose one primary mode: onboarding, concept, project, practice, review, debug, or calibration.
4. Teach with cognitive positioning, prior-knowledge mapping, a minimal runnable example, practical usage, best practices, pitfalls, and recall.
5. Generate one focused next task instead of a large roadmap unless the user asks for a roadmap.
6. Persist or summarize state updates at the end of the turn.

## Persistence Commands

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json profile --known-stack JavaScript TypeScript React
python -m learning_accelerator.cli --state-file .learning/state.json topic "FastAPI dependency injection" --level beginner
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json due
```

## Compatibility Notes

- Codex: copy this directory to `~/.codex/skills/learning-accelerator`.
- Claude Code: copy this directory to `~/.claude/skills/learning-accelerator` or keep this `CLAUDE.md` as project memory.
- Cursor, Windsurf, Aider, and other coding agents: point project rules or custom instructions at this `AGENTS.md`, `SKILL.md`, or `SYSTEM_PROMPT.md`.
- Generic LLM apps: paste `SYSTEM_PROMPT.md` as system instructions and use the JSON schema in `references/learning_os_protocol.md` for state.
