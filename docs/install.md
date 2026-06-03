# Installation Guide

Learning Accelerator is designed to be installed as a skill root. The repository root contains `SKILL.md`, so a published GitHub repository can be installed directly without first copying files by hand.

## Recommended: Install From GitHub In Codex

After publishing this repository to GitHub, ask Codex to install it with the built-in skill installer:

```text
Use skill-installer to install the skill from https://github.com/<owner>/<repo>.
```

If the skill lives in a subdirectory instead of the repository root, provide the tree URL:

```text
Use skill-installer to install the skill from https://github.com/<owner>/<repo>/tree/main/<path-to-skill>.
```

After installation, restart Codex so it can load the new skill.

## Public Ecosystem: skills.sh

skills.sh is the public agent skills directory. If Learning Accelerator is published there, users can discover and install it with the Skills CLI:

```bash
npx skills find learning accelerator
npx skills add <owner>/Learning-Accelerator
```

The public skill page should look like:

```text
https://skills.sh/<owner>/Learning-Accelerator
```

If `npx skills find learning accelerator` does not return this project, it has not been indexed by skills.sh yet. In that case, use the GitHub URL installation path above.

Codex `skill-installer` and `npx skills` are complementary:

- `skill-installer` is convenient inside Codex when you already know the GitHub repository URL.
- `npx skills find` is better for public discovery across Claude Code, Cursor, Codex, Gemini, and other compatible agents.
- `npx skills add` is the cross-agent one-command install path once the skill is published in the public ecosystem.

## Local Development Install

Use manual copy only when developing the skill locally or testing unpublished changes.

```bash
rm -rf ~/.codex/skills/learning-accelerator
mkdir -p ~/.codex/skills/learning-accelerator
cp -R SKILL.md SYSTEM_PROMPT.md README.md manifest.json AGENTS.md CLAUDE.md GEMINI.md agents examples references learning_accelerator pyproject.toml docs \
  ~/.codex/skills/learning-accelerator/
```

Restart Codex after copying.

## Claude Code

Claude Code can use either the skill directory or project memory:

```bash
rm -rf ~/.claude/skills/learning-accelerator
mkdir -p ~/.claude/skills/learning-accelerator
cp -R SKILL.md SYSTEM_PROMPT.md README.md manifest.json AGENTS.md CLAUDE.md GEMINI.md agents examples references learning_accelerator pyproject.toml docs \
  ~/.claude/skills/learning-accelerator/
```

For project-level usage, keep `CLAUDE.md` in the project root.

## Cursor

Copy the Cursor rule into a target project:

```bash
mkdir -p .cursor/rules
cp .cursor/rules/learning-accelerator.mdc <target-project>/.cursor/rules/
```

## Gemini CLI

Keep `GEMINI.md` in the repository root. When the full behavior contract is needed, also load `SYSTEM_PROMPT.md` and `references/learning_os_protocol.md`.

## Generic Agents

Use these entry points:

- `AGENTS.md` for coding agents that read project instructions.
- `SYSTEM_PROMPT.md` for agents that only support system or developer prompts.
- `references/learning_os_protocol.md` for state schema and operating protocol.

## Python CLI

Install the CLI locally when you want to call `learning-accelerator` directly:

```bash
python -m pip install -e .
learning-accelerator --state-file .learning/state.json show
```

For tests:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

If editable install fails on an old pip version, upgrade pip first:

```bash
python -m pip install --upgrade pip
```
