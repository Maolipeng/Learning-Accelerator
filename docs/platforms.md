# Platform Compatibility

Learning Accelerator can be used as a skill, project memory file, system prompt, or local JSON state utility depending on the host tool.

## Compatibility Matrix

| Platform | Status | Primary Entry | Install or Configuration |
|---|---|---|---|
| Codex | Supported | `SKILL.md`, `agents/openai.yaml` | Copy this directory to `~/.codex/skills/learning-accelerator`. |
| Claude Code | Supported | `CLAUDE.md`, `SKILL.md` | Copy this directory to `~/.claude/skills/learning-accelerator`, or keep `CLAUDE.md` in a project. |
| Cursor | Supported through rules | `.cursor/rules/learning-accelerator.mdc` | Keep the rule file in the repository or copy it into a Cursor project. |
| Gemini CLI | Supported through project guide | `GEMINI.md`, `SYSTEM_PROMPT.md` | Keep `GEMINI.md` in the repository and load `SYSTEM_PROMPT.md` when full instructions are needed. |
| OpenAI-style skill loaders | Supported | `SKILL.md`, `manifest.json`, `agents/openai.yaml` | Load the skill root and read the manifest metadata. |
| Generic coding agents | Supported | `AGENTS.md` | Point project instructions at `AGENTS.md`, then load `SKILL.md` or `SYSTEM_PROMPT.md` as needed. |
| Generic LLM apps | Supported | `SYSTEM_PROMPT.md` | Paste `SYSTEM_PROMPT.md` into system or developer instructions. |

## Required Files By Mode

Skill mode:

- `SKILL.md`
- `references/learning_os_protocol.md`
- `examples/`
- `learning_accelerator/` when local JSON persistence is desired

Project guide mode:

- `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`
- `SYSTEM_PROMPT.md`
- `references/learning_os_protocol.md`

CLI persistence mode:

- `learning_accelerator/state.py`
- `learning_accelerator/cli.py`
- `pyproject.toml`

## Recommended State Path

Use project-local state when the learning context belongs to one repository:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
```

Use the default user-level path when the learning context should follow the learner across projects:

```bash
learning-accelerator show
```

The default path is `~/.learning-accelerator/state.json`.

