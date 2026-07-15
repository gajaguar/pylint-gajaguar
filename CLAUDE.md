# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this repo is

A **pylint plugin** ("pylint-plugin") encoding personal code-review preferences
that ruff doesn't cover. The plugin entrypoint is `register(linter)` in
`src/main.py`, which instantiates and registers every checker in
`src/checkers/`.

`src/` is a **flat layout**: `pyproject.toml`'s
`[tool.hatch.build.targets.wheel]` sets `packages = ["src/checkers"]`, `include
= ["src/main.py"]`, and `sources = ["src"]`, so `main.py` and `checkers/` are
top-level importable modules — there is no wrapping package directory. Imports
inside `main.py` are `from checkers.x import Y`.

`[project.scripts] app = "main:main"` in `pyproject.toml` is dead — `main.py`
exposes `register`, not `main`. Pre-existing issue, not introduced by the
flattening; flag before fixing.

## Self-linting

`make pylint` and the pre-commit `pylint` hook load `--load-plugins=main` — this
repo's own local `checkers/`, installed editable via `uv sync` (see the
flat-layout build config above). It does **not** load a published
`pylint_plugin` package; there is no such distribution installed or pinned in
`[tool.uv.sources]`. Downstream consumers of this plugin (per the README's
"Usage" pattern) load it as `pylint_plugin` once published — don't conflate that
consumer-facing name with the local self-check, which always uses `main`.

## Commands

```bash
make install   # set up the full dev environment (deps, console scripts, git hooks)
make check     # run the full read-only validation gate (fails on any violation)
make fix       # apply all safe auto-fixes in place
make test      # run the test suite
make help      # full target list
```

- Every quality target accepts `FILES="..."` to scope to paths/globs, e.g. `make
  lint FILES="src/main.py"`, `make test FILES="tests/test_x.py"`.
- Targets split by mutation: `check`-family is read-only (the CI gate);
  `fix`-family writes in place. `fix-unsafe` additionally applies ruff's unsafe
  fixes.
- Single test: `make test FILES="tests/test_foo.py::TestClass::test_case"`.

## Architecture

Each checker is a `BaseChecker` (or `BaseTokenChecker`) subclass in its own file
under `src/checkers/`, following pylint's visitor pattern (`visit_functiondef`,
`visit_importfrom`, token streams, etc.). Adding a checker requires two edits:

1. Create `src/checkers/<rule>.py` with the checker class.
2. Register it in `src/main.py`'s `register()` **and** add its `name` to the
   `PYLINT_RULES` list in the `Makefile` and the `--enable=` list in
   `.pre-commit-config.yaml` (both hardcode the enabled rule set).

Conventions across checkers:

- `name` is `app-<kebab-rule>`; message symbols reuse that same `app-*` string.
- Message codes live in the `9xxx` custom range (`W9001`, `C9005`, …). `msgs`
  dicts carry `# noqa: RUF012` (mutable class attr).
- `smoke.py` (`SmokeChecker`) is an empty checker with no messages — a
  registration smoke test; keep it registered.
- Checkers that need source text (not just the AST) read the file themselves and
  cache lines per-file (see `test_aaa_markers.py`).

Registered rules:

| Rule (`name`)                 | Code  | Enforces                                                        |
| ----------------------------- | ----- | --------------------------------------------------------------- |
| `app-no-docstrings`           | W9001 | No docstrings on functions/methods/classes (use comments)       |
| `app-test-aaa-markers`        | W9002 | `test_*` bodies contain `# Arrange`, `# Act`, `# Assert`        |
| `app-test-no-blank-lines`     | W9003 | No blank lines inside test method bodies                        |
| `app-unused-arg-use-del`      | W9004 | Use `del arg` at body top, not a `_`-prefixed arg               |
| `app-module-const-naming`     | C9005 | Module-level names are `SCREAMING_SNAKE_CASE`                   |
| `app-no-file-level-disable`   | W9006 | No standalone `# pylint: disable=`; use inline / `disable-next` |
| `app-no-inline-imports`       | W9008 | Imports at module top, not inside functions                     |
| `app-no-relative-imports`     | W9009 | Absolute imports only                                           |
| `app-use-contextlib-suppress` | W9012 | `contextlib.suppress(...)` over `try/except/pass`               |
| `app-frozenset-constant`      | W9013 | Module-level set constants use `frozenset(...)`                 |
| `app-require-final`           | C9014 | Module-level constants carry a `Final` annotation               |

`make pylint` deliberately runs `--disable=all` then `--enable=` only these
`app-*` rules: pylint's built-ins overlap with ruff or conflict with these rules
(e.g. `missing-module-docstring` vs. `app-no-docstrings`).

## Project conventions (this repo dogfoods its own rules)

- **No docstrings.** Comments only, and only where the *why* isn't obvious.
  Pylint's W9001 can only report, not fix — remove docstrings manually.
- **Absolute imports only**, imports at module top, one import per line (`ruff
  isort force-single-line`).
- ruff runs with `lint.select = ["ALL"]` and a curated ignore list; line length
  119. mypy is `strict` (tests excluded); pyright covers `src` only.
- `tests/` currently holds only `__init__.py` — no test suite exists yet. Test
  files mirror `src/` and must satisfy the AAA-marker and no-blank-line rules
  above.
