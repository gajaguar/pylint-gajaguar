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
- **pylint** + [`pylint-plugin`](https://github.com/gajaguar/pylint-plugin) (uv
  git dependency) — custom checkers for personal-preference rules ruff doesn't
  cover (e.g. no docstrings — see below). Check-only: pylint has no autofix.
- **pre-commit** — git hook running ruff, ruff-format, mypy, and pylint before
  each commit

### Docstring policy

This project does not use docstrings — use comments only where the *why* isn't
obvious from the code. `pylint-plugin`'s `app-no-docstrings` (W9001) checker
fails `make check`/`make pylint` if any function, method, or class has one;
remove docstrings manually.

### Custom pylint checkers (`pylint-plugin`)

A standalone pylint plugin encoding personal code-review preferences beyond
ruff's rule set, installed as a `uv` git dependency pinned in `pyproject.toml`'s
`[tool.uv.sources]` — see [the plugin's
README](https://github.com/gajaguar/pylint-plugin) for the full checker list.
It's a separate repo, not vendored, so the same rules can be reused and updated
across every project built from this template without copy-pasting checker code.

## Using this as a template

`src/` is a flat layout (`sources = ["src"]` in `pyproject.toml`): `main.py` and
`checkers/` are top-level importable modules, not wrapped in a package
directory. To start a real project:

1. Update `[project].name` and `[project.scripts]` in `pyproject.toml`.
2. Update this README and `LICENSE` copyright holder if needed.
3. Run `make install && make check && make test` to confirm everything still
   passes.

## Project layout

```text
.
├── pyproject.toml   # deps, ruff/mypy/pyright/pytest/coverage config
├── Makefile          # check/fix command surface
├── scripts/            # docstring-stripping script (pylint has no autofix)
├── src/                # flat source layout: main.py + checkers/
└── tests/              # test suite (mirrors src/)
```
