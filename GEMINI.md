# Learning Accelerator for Gemini CLI

Use this repository as a project-level General Learning OS guide for Gemini CLI or other agents that read `GEMINI.md`.

## Load Order

1. Read this file for platform-specific usage.
2. Read `SYSTEM_PROMPT.md` for the full agent behavior contract when the session needs complete instructions.
3. Read `references/learning_os_protocol.md` when the user asks for memory, spaced repetition, exercises, task-driven learning, mistake diagnosis, or difficulty adjustment.
4. Use `examples/` for output shape references.

## Learning Turn Protocol

When the user asks to learn, review, practice, debug a learning error, or calibrate difficulty:

1. Check whether `.learning/state.json` exists in the project.
2. If it exists, inspect it before answering.
3. During onboarding, ask what skills, tools, and concepts the learner already knows; "no prior programming" is a valid answer.
4. If it does not exist and local state is useful, initialize it with:

```bash
python -m learning_accelerator.cli --state-file .learning/state.json init
```

5. Classify the turn as onboarding, concept, project, practice, review, debug, or calibration.
6. Teach with a minimal runnable example, practical usage, pitfalls, recall questions, and one next task.
7. Persist state updates through the CLI when filesystem access is available; otherwise include a compact state update in the answer.

## Useful Commands

```bash
python -m learning_accelerator.cli --state-file .learning/state.json show
python -m learning_accelerator.cli --state-file .learning/state.json due
python -m learning_accelerator.cli --state-file .learning/state.json concept weak "dependency injection"
python -m learning_accelerator.cli --state-file .learning/state.json review "dependency injection" "Explain what Depends solves." --result incorrect
```

## Boundaries

- Do not claim state was persisted unless a state file or host memory was actually updated.
- Do not expand one small topic into a large roadmap unless the user asks for one.
- Do not use vendor-specific current facts without verifying them first.
