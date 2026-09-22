# Custom Pylint Rules

Plugin with a series of rules based on good practices and personal tastes.

## Quickstart

```bash
make install   # sync Python deps, install node tooling, install pre-commit hook
make check     # read-only gate: lint, format-check, mypy, pyright, md-lint, spell
make fix       # apply safe auto-fixes (format, ruff --fix, markdownlint --fix)
make test      # run the test suite
```

Run `make help` for the full target list.

## Command convention: `check` vs `fix`

Targets are split by whether they mutate files:

| Prefix / umbrella   | Behavior                                                             | Example targets                                                                               |
| ------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `check` (read-only) | Reports problems, exits non-zero, never writes. This is the CI gate. | `lint`, `format-check`, `mypy`, `pyright`, `typecheck`, `md-lint`, `spell`, `pylint`, `check` |
| `fix` (writable)    | Mutates files in place.                                              | `format`, `lint-fix`, `lint-fix-unsafe`, `md-fix`, `fix`, `fix-unsafe`                        |

All targets accept `FILES="..."` to scope to specific paths/globs, e.g. `make
lint FILES="src/main.py"`.

## Toolchain

- **uv** — dependency management and virtualenvs (`hatchling` build backend)
- **ruff** — linting and formatting (`lint.select = ["ALL"]`, curated ignores)
- **mypy** + **pyright** — static type checking
- **pytest** + **pytest-cov** — testing and coverage
- **markdownlint-cli2** + **cspell** (pnpm, dev-only) — Markdown lint & spell
  check
- **pylint** — runs this repo's own checkers against itself
  (`--load-plugins=main`, see below). Check-only: pylint has no autofix.
- **pre-commit** — git hook running ruff, ruff-format, mypy, and pylint before
  each commit

### Docstring policy

This project does not use docstrings — use comments only where the *why* isn't
obvious from the code. `app-no-docstrings` (W9001) fails `make check`/`make
pylint` if any function, method, or class has one; remove docstrings manually.

### Custom pylint checkers

A pylint plugin encoding personal code-review preferences beyond ruff's rule
set. `src/main.py` exposes `register(linter)`, which registers every checker in
`src/checkers/`. `make pylint` self-lints this repo with those same checkers
(`--load-plugins=main --disable=all --enable=<the app-* rules>`).

| Rule (`name`)                         | Code  | Enforces                                                         |
| -------------------------------------- | ----- | ----------------------------------------------------------------- |
| `app-no-docstrings`                   | W9001 | No docstrings on functions/methods/classes (use comments)        |
| `app-test-aaa-markers`                | W9002 | `test_*` bodies contain `# Arrange`, `# Act`, `# Assert`         |
| `app-test-no-blank-lines`             | W9003 | No blank lines inside test method bodies                         |
| `app-test-no-extra-comments`          | W9015 | Test bodies carry only the configured section markers            |
| `app-test-partial-assertion`          | W9016 | Field assertions without a whole-object assertion (advisory)     |
| `app-test-name-implementation-detail` | W9017 | Test names naming mocks, patches, internals (advisory)           |
| `app-unused-arg-use-del`              | W9004 | Use `del arg` at body top, not a `_`-prefixed arg                |
| `app-module-const-naming`             | C9005 | Module-level names are `SCREAMING_SNAKE_CASE`                    |
| `app-no-file-level-disable`           | W9006 | No standalone `# pylint: disable=`; use inline / `disable-next`  |
| `app-no-inline-imports`               | W9008 | Imports at module top, not inside functions                      |
| `app-no-relative-imports`             | W9009 | Absolute imports only                                            |
| `app-use-contextlib-suppress`         | W9012 | `contextlib.suppress(...)` over `try/except/pass`                |
| `app-frozenset-constant`              | W9013 | Module-level set constants use `frozenset(...)`                  |
| `app-require-final`                   | C9014 | Module-level constants carry a `Final` annotation                |

`app-test-partial-assertion` and `app-test-name-implementation-detail` are
heuristics with a real false-positive rate — treat them as advisory, not a hard
gate.

## Usage in another project

Add this repo as a `uv` git dependency and load it as a pylint plugin:

```toml
[dependency-groups]
dev = ["pylint-plugin @ git+https://github.com/gajaguar/pylint-plugin"]
```

```bash
pylint --load-plugins=main --disable=all --enable=app-no-docstrings,... src tests
```

## Project layout

```text
.
├── pyproject.toml   # deps, ruff/mypy/pyright/pytest/coverage config
├── Makefile          # check/fix command surface
├── src/                # flat source layout: main.py + checkers/
└── tests/              # test suite (mirrors src/)
```
