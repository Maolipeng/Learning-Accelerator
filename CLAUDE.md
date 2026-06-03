# Learning Accelerator for Claude Code

Use this repository as a reusable General Learning OS inside Claude Code. It can run as a Claude Code skill, a project memory file, or a plain system prompt source.

## Primary Entry

- Prefer `SKILL.md` when Claude Code skills are available.
- Use `SYSTEM_PROMPT.md` when the environment only supports project or session instructions.
- Load `references/learning_os_protocol.md` when the user asks for learning state, spaced repetition, exercises, mistake diagnosis, task-driven learning, or difficulty adjustment.

## Claude Code Skill Install

Copy the repository into a Claude Code skill directory, keeping `SKILL.md` at the skill root:

```bash
mkdir -p ~/.claude/skills
cp -R Learning-Accelerator ~/.claude/skills/learning-accelerator
```

If copying from inside the repository, copy only the runtime files:

```bash
rm -rf ~/.claude/skills/learning-accelerator
mkdir -p ~/.claude/skills/learning-accelerator
cp -R SKILL.md SYSTEM_PROMPT.md README.md manifest.json agents examples references learning_accelerator pyproject.toml \
  ~/.claude/skills/learning-accelerator/
```

## Runtime State

When local filesystem access is available, persist learning state with the bundled CLI:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
python -m learning_accelerator.cli --state-file .learning/state.json show
python -m learning_accelerator.cli --state-file .learning/state.json due
```

Use `.learning/state.json` for project-local learning state, or the default `~/.learning-accelerator/state.json` for user-level state.

## Operating Rules

- Default to Chinese when the user writes Chinese.
- During onboarding, ask what skills, tools, and concepts the learner already knows; no prior programming is a valid answer.
- Start each learning turn by checking existing state when storage is available.
- Classify the turn as onboarding, concept, project, practice, review, debug, or calibration.
- Teach through positioning, analogy, minimal runnable examples, engineering usage, pitfalls, recall, and one next action.
- Update mastered concepts, weak concepts, misconceptions, review items, project tasks, and difficulty evidence after each learning turn.
- Do not claim persistence happened unless a local state file or host memory was actually updated.
