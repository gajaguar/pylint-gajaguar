# AGENTS.md

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Agent instructions

`AGENTS.md` is the only agent instructions file. The repository MUST NOT
contain a `CLAUDE.md` or any other tool-specific copy; project rules go here.

## What this is

A pylint plugin that adds 14 opinionated checkers (`gajaguar-*` rules) encoding
personal review preferences that ruff's `lint.select = ["ALL"]` doesn't
cover: no docstrings, mandatory AAA section markers in tests, `Final` on
module constants, etc. The plugin self-lints this repo — `make pylint`
runs the rules it defines against `src` and `tests`, so a regression in
the plugin fails the same gate it defines.

## Command surface

The agent MUST use the `Makefile` targets (`make check`, `make fix`,
`make test`, ...) instead of invoking the underlying tools directly, and
MUST NOT add a target without its `##` help line. Run `make help` for the
full list.

Scope any target to specific files with `FILES=`:

```bash
make lint FILES="src/pylint_gajaguar/scopes.py"
make pylint FILES="src"
make pytest FILES="tests/checkers/test_scopes.py::test_name -x"
```

Override the AAA section markers without touching config:

```bash
TEST_SECTION_MARKERS="Given When Then" make pylint
```

`check`/`fix` are always split: `check*` targets are read-only and exit
non-zero on problems (the CI gate); `fix*` targets mutate files in place.

## Gate

`make check` MUST pass before any commit. Findings SHOULD be fixed with
`make fix` before editing by hand.

## Commits and branches

Commit messages MUST follow
[Conventional Commits](https://www.conventionalcommits.org/); branch names
MUST follow [Conventional Branch](https://conventionalbranch.org/)
(`<type>/<description>`, e.g. `feat/add-checker`, `fix/frozenset-false-positive`).
A commit type may be any Conventional Commits type, but a branch type MUST
be one of `feat` (or `feature`), `fix` (or `bugfix`), `hotfix`, `release`,
`chore`; documentation and dependency work uses `chore/`, e.g.
`chore/update-readme`. A pre-commit hook and `make commits-check` enforce
both — see
[`docs/conventions/commits-check.md`](docs/conventions/commits-check.md).

Scope checker and checker-test edits to one checker per change.

## Documentation

Documentation MUST be an OKF bundle of atomic notes under `docs/`: one
Markdown concept per file, with YAML frontmatter (`type`, `title`,
`description`). A new note MUST be added to its directory's `index.md` and
to [`docs/log.md`](docs/log.md). A note MUST cover exactly one concept, and
only when it explains something a reader can't already get from `make
help`, a linter's own message, or the configuration it comes from.

## Dependencies

A new tool MUST be added to the ecosystem manager that owns it and MUST
only go in `mise.toml` when it bootstraps an ecosystem or has none in this
repository — see
[`docs/toolchain/layering-rule.md`](docs/toolchain/layering-rule.md).

## Architecture

```text
pylint --load-plugins=pylint_gajaguar
  -> src/pylint_gajaguar/__init__.py (re-exports register)
    -> pylint_gajaguar/_register.py: register(linter)
      -> instantiates and registers each Checker class
scopes.py -> shared section-marker option + test-scoping helpers,
             consumed by gajaguar-test-* checkers
```

The distribution is `pylint-gajaguar` and the single top-level package is
`pylint_gajaguar`: `[tool.hatch.build.targets.wheel]` sets
`sources = ["src"]`, so `src/pylint_gajaguar/` installs as
`pylint_gajaguar`. That's why `--load-plugins=pylint_gajaguar` resolves,
and why in-repo imports read `from pylint_gajaguar.foo import Bar` rather
than `from src.pylint_gajaguar.foo import Bar`.

Pylint's plugin loading and the messages-control disable list live in
`pyproject.toml` (`[tool.pylint.main]`, `[tool.pylint."messages
control"]`) — not passed as CLI flags — so `mk/python.mk`'s `pylint`
target and the pre-commit `pylint` hook stay in sync with each other by
construction.

## Adding a checker (three-file procedure)

Keep these in order; each new checker gets its own scoped commit/PR:

1. **`src/pylint_gajaguar/<name>.py`** — subclass `pylint.checkers.BaseChecker`,
   set a unique `name = "gajaguar-..."` and message code. Group test-related
   checkers around the helpers in `src/pylint_gajaguar/scopes.py`
   (`is_test_file`, `is_test_function`, `section_markers`).
2. **`src/pylint_gajaguar/_register.py`** — import the new checker and add
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

`gajaguar-test-*` checkers only activate on files where the stem starts with
`test_`, ends with `_test`, or a parent directory is named `test`/`tests`
(`scopes.is_test_file`). Within a test file, only `test_*`-named
functions are checked (`scopes.is_test_function`); helpers in the same
file are not. Non-test-scoped checkers (`gajaguar-no-docstrings`,
`gajaguar-module-const-naming`, `gajaguar-require-final`, etc.) apply everywhere.

## Python

- The agent MUST NOT add docstrings to functions, methods, or classes; use a
  comment only where the *why* is not obvious from the code. The plugin's own
  `gajaguar-no-docstrings` checker enforces this and fails
  `make check`/`make pylint` otherwise; pylint has no autofix for it, so
  remove docstrings by hand.
- Every `gajaguar-*` rule MUST be enabled in `pyproject.toml`'s
  `[tool.pylint."messages control"].enable`; `make pylint-rules` (part of
  `make check`) fails and lists any that are missing.
- `conventional-git` MUST be the latest PyPI release; `make
  conventional-git-latest` (part of `make check`) fails otherwise, and `make
  install` upgrades it.
- The agent MUST NOT add a `pyproject.toml` setting that equals the tool's
  default, and every `lint.per-file-ignores` entry MUST match a current
  violation — see
  [`docs/python/pyproject-defaults.md`](docs/python/pyproject-defaults.md).
- The agent MUST run `make check` and `make test` before committing Python
  changes, and SHOULD run `make fix` first for anything auto-fixable.

### Conventions specific to this repo

- Absolute imports only (`gajaguar-no-relative-imports`):
  `from pylint_gajaguar.foo import Bar`, not `from .foo import Bar`.
- Module-level constants: `SCREAMING_SNAKE_CASE` name
  (`gajaguar-module-const-naming`) and a `Final` annotation
  (`gajaguar-require-final`); module-level set constants must be
  `frozenset(...)` (`gajaguar-frozenset-constant`).
- No standalone `# pylint: disable=` — use inline or
  `disable-next` (`gajaguar-no-file-level-disable`).
- Imports live at module top, never inside functions
  (`gajaguar-no-inline-imports`).
- `contextlib.suppress(...)` over `try/except/pass`
  (`gajaguar-use-contextlib-suppress`).
- Test bodies: exactly the configured AAA section markers (default `#
  Arrange` / `# Act` / `# Assert`) as comments, no blank lines, no extra
  comments (`gajaguar-test-aaa-markers`, `gajaguar-test-no-blank-lines`,
  `gajaguar-test-no-extra-comments`). `gajaguar-test-partial-assertion` and
  `gajaguar-test-name-implementation-detail` are advisory heuristics with a
  known false-positive rate — not hard gates.
- Ruff `lint.select = ["ALL"]`; justified ignores use `# noqa: <rule>`
  inline. mypy runs `strict`; pyright is clean on `src` (tests excluded
  from both).
