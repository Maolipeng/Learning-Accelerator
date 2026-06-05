# Release Guide

This project uses manual versioning plus a tag-triggered GitHub Actions workflow.

## Release Checklist

1. Confirm version numbers match:

```bash
python -m learning_accelerator.cli version
rg 'version =|\"version\"|__version__' pyproject.toml manifest.json learning_accelerator/__init__.py
```

2. Update `CHANGELOG.md`.

Move completed changes from `Unreleased` into the release version section, for example `v1.6.0`.

3. Run local verification:

```bash
python -m pytest
git diff --check
python -m json.tool manifest.json >/dev/null
python -m json.tool schemas/learning_state.schema.json >/dev/null
```

4. Create and push a tag:

```bash
git tag v1.6.0
git push origin v1.6.0
```

5. Watch `.github/workflows/release.yml`.

The `release.yml` workflow runs tests, builds the source distribution and wheel, then uploads the `dist/` artifact. It does not publish to PyPI automatically.

6. Verify the artifact.

Download the workflow artifact and inspect:

```bash
python -m tarfile --list dist/learning_accelerator-*.tar.gz | head
python -m zipfile --list dist/learning_accelerator-*.whl | head
```

7. Create the GitHub Release.

Use the tag name, attach the artifact if desired, and paste the `CHANGELOG.md` section for the release.

## Version Boundaries

- `pyproject.toml` controls Python package metadata.
- `learning_accelerator.__version__` powers `learning-accelerator version`.
- `manifest.json` advertises the skill/package version to agent ecosystems.
- `SCHEMA_VERSION` in `learning_accelerator.state` is the persisted state schema version and should not change for feature-only releases.

## Non-goals

- No automatic PyPI publish yet.
- No signed artifacts yet.
- No generated GitHub release notes yet.
