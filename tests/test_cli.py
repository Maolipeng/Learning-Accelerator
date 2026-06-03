from __future__ import annotations

import json

from learning_accelerator.cli import main


def test_cli_profile_topic_review_and_due(tmp_path, capsys):
    state_file = tmp_path / "state.json"

    assert main(["--state-file", str(state_file), "init"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "profile",
        "--known-stack",
        "TypeScript",
        "React",
        "--goal",
        "Learn FastAPI",
    ]) == 0
    assert main(["--state-file", str(state_file), "topic", "FastAPI", "--level", "beginner"]) == 0
    assert main(["--state-file", str(state_file), "concept", "weak", "dependency injection"]) == 0
    assert main([
        "--state-file",
        str(state_file),
        "review",
        "dependency injection",
        "Explain Depends in one sentence.",
        "--result",
        "incorrect",
    ]) == 0
    assert main(["--state-file", str(state_file), "due", "--date", "2999-01-01"]) == 0

    output = capsys.readouterr().out.strip().splitlines()
    due_json_start = next(i for i in range(len(output) - 1, -1, -1) if output[i] == "[")
    due_items = json.loads("\n".join(output[due_json_start:]))
    assert due_items[0]["concept"] == "dependency injection"
