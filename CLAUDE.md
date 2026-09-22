# AGENTS.md

## What this is

A pylint plugin that adds 14 opinionated checkers (`app-*` rules) encoding
personal review preferences that ruff's `lint.select = ["ALL"]` doesn't
cover: no docstrings, mandatory AAA section markers in tests, `Final` on
module constants, etc. The plugin self-lints this repo — `make pylint`
runs the rules it defines against `src` and `tests`, so a regression in
the plugin fails the same gate it defines.

## Commands

```bash
make install          # sync venv, Node tooling (pnpm), pre-commit hook
make check             # gate: lint, md-lint, spell, mypy, pyright, pylint
make fix               # apply safe auto-fixes
make fix-unsafe        # apply all auto-fixes, including unsafe ones
make test              # run pytest (with coverage)
make pylint            # run just the plugin's own checkers against src/tests
make help              # list every target
```

Scope any target to specific files with `FILES=`:

```bash
make lint FILES="src/checkers/scopes.py"
make pylint FILES="src"
make md-lint FILES="README.md"
```

Run a single test:

```bash
uv run pytest tests/checkers/test_scopes.py::test_name -x
```

Override AAA section markers without touching config:

```bash
TEST_SECTION_MARKERS="Given When Then" make pylint
```

`check`/`fix` are always split: `check*` targets are read-only and exit
non-zero on problems (the CI gate); `fix*` targets mutate files in place.

## Architecture

```text
pylint --load-plugins=main
  -> src/main.py (re-exports register)
    -> checkers/_register.py: register(linter)
      -> instantiates and registers each Checker class
scopes.py -> shared section-marker option + test-scoping helpers,
             consumed by app-test-* checkers
```

The wheel ships a **flat layout**: `[tool.hatch.build.targets.wheel]` sets
`sources = ["src"]`, so `src/main.py` and `src/checkers/` install as
top-level modules (`main`, `checkers`), not a nested `pylint_plugin`
package. That's why `--load-plugins=main` resolves, and why in-repo
imports read `from checkers.foo import Bar` rather than
`from src.checkers.foo import Bar`.

Pylint's plugin loading and the messages-control disable list live in
`pyproject.toml` (`[tool.pylint.main]`, `[tool.pylint."messages
control"]`) — not passed as CLI flags — so `mk/python.mk`'s `pylint`
target and the pre-commit `pylint` hook stay in sync with each other by
construction.

## Adding a checker (three-file procedure)

Keep these in order; each new checker gets its own scoped commit/PR:

1. **`src/checkers/<name>.py`** — subclass `pylint.checkers.BaseChecker`,
   set a unique `name = "app-..."` and message code. Group test-related
   checkers around the helpers in `src/checkers/scopes.py`
   (`is_test_file`, `is_test_function`, `section_markers`).
2. **`src/checkers/_register.py`** — import the new checker and add
   `linter.register_checker(NewChecker(linter))` inside `register()`.
   Order is cosmetic but kept stable.
3. **`tests/checkers/test_<name>.py`** — use
   `pylint.testutils.CheckerTestCase` and the builders in
   `tests/conftest.py`: `build_module_from_source` for ordinary modules,
   `build_test_module_from_source` when the checker is test-scoped (so
   the built filename starts with `test_`), and `node_position` to derive
   the expected message span from a node's header position (not its full
   body span — pylint reports `FunctionDef`/`ClassDef` messages against
   `node.position`).

After the three-file edit, run `make check` and `make test` from the
repo root — `make check` runs the new rule against the plugin's own
source via `make pylint`, so a rule that the plugin's own code violates
surfaces immediately.

## Test scoping

`app-test-*` checkers only activate on files where the stem starts with
`test_`, ends with `_test`, or a parent directory is named `test`/`tests`
(`scopes.is_test_file`). Within a test file, only `test_*`-named
functions are checked (`scopes.is_test_function`); helpers in the same
file are not. Non-test-scoped checkers (`app-no-docstrings`,
`app-module-const-naming`, `app-require-final`, etc.) apply everywhere.

## Conventions specific to this repo

- **No docstrings anywhere** (including on new checkers/tests) —
  `app-no-docstrings` fails `make check` on any. Comments only when the
  _why_ isn't obvious from the code; pylint has no autofix for this, so
  remove docstrings by hand.
- Absolute imports only (`app-no-relative-imports`); `from checkers.foo
import Bar`, not `from .foo import Bar`.
- Module-level constants: `SCREAMING_SNAKE_CASE` name
  (`app-module-const-naming`) and a `Final` annotation
  (`app-require-final`); module-level set constants must be
  `frozenset(...)` (`app-frozenset-constant`).
- No standalone `# pylint: disable=` — use inline or
  `disable-next` (`app-no-file-level-disable`).
- Imports live at module top, never inside functions
  (`app-no-inline-imports`).
- `contextlib.suppress(...)` over `try/except/pass`
  (`app-use-contextlib-suppress`).
- Test bodies: exactly the configured AAA section markers (default `#
Arrange` / `# Act` / `# Assert`) as comments, no blank lines, no extra
  comments (`app-test-aaa-markers`, `app-test-no-blank-lines`,
  `app-test-no-extra-comments`). `app-test-partial-assertion` and
  `app-test-name-implementation-detail` are advisory heuristics with a
  known false-positive rate — not hard gates.
- Ruff `lint.select = ["ALL"]`; justified ignores use `# noqa: <rule>`
  inline. mypy runs `strict`; pyright is clean on `src` (tests excluded
  from both).
- Toolchain layering (see `docs/toolchain.md`): mise pins what bootstraps
  an ecosystem or belongs to none (node, pnpm, python, uv, checkmake,
  pre-commit); each ecosystem's own package manager installs everything
  else (`package.json`/pnpm for cspell/markdownlint-cli2,
  `pyproject.toml`/uv for ruff/mypy/pyright/pytest/pylint). Don't add a
  tool to `mise.toml` if it belongs to an existing ecosystem's lockfile.
- Commits: Conventional Commits. Branches: Conventional Branch.
- Scope checker/checker-test edits to one checker per change.
