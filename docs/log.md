# Directory Update Log

## 2026-10-02

* **Change**: the first `make docs-retag` run re-assigned the tags of several
  notes.
* **Addition**: `okf-base.yaml`, `make docs-lint`, `tools/docs-retag.py`,
  `conventions/tag-vocabulary.md` and `toolchain/retag-notes.md`.
* **Addition**: `conventions/versioning.md` sets the SemVer bump criteria, tags
  only minor and major bumps, and leaves releases on demand.
* **Addition**: `AGENTS.md` links to `conventions/versioning.md`.
* **Change**: `conventions/tag-vocabulary.md` states the tag form: lowercase, one
  word by default, no parent prefix.
* **Addition**: `make release-tag` (`mk/python.mk`) tags the base branch as
  `v<project.version>` after a minor or major bump merges.
* **Change**: `conventions/versioning.md` names `make release-tag` as the way to
  tag where the `Makefile` defines it.

## 2026-09-30

* **Addition**: [`conventions/help-check.md`](conventions/help-check.md) and
  [`conventions/claude-md-check.md`](conventions/claude-md-check.md) document
  the `make help-check` and `make claude-md-check` targets that `make check`
  now runs.
* **Change**: [`conventions/commits-check.md`](conventions/commits-check.md)
  states that `make commits-check` skips merge commits, and the branch-type
  rule for documentation and dependency work.

## 2026-09-29

* **Change**: The pre-commit hooks and `CONVENTIONAL_GIT` now run
  `uvx conventional-git@latest`, the dev dependency requires
  `conventional-git>=1.1`, and the `dependabot/*` skip in
  `make commits-check` is gone: 1.1.0 accepts `dependabot/` and `renovate/`
  branch names itself. Updated
  [`conventions/commits-check.md`](conventions/commits-check.md).

## 2026-09-28

* **Addition**: Added PyPI Trusted Publishing under `release/`.
* **Restructure**: Replaced the flat `conventions.md`, `python.md` and
  `toolchain.md` with one note per concept under `conventions/`,
  `toolchain/` and `python/`, each listed in its directory `index.md`.
