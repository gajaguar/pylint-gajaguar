# AGENTS.md

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Agent instructions

- `AGENTS.md` is the only agent instructions file; put project rules here. The
  repository MUST NOT contain a `CLAUDE.md` or any other tool-specific copy,
  because a second copy drifts from this one; `make claude-md-check` fails on
  one.

## What this is

A pylint plugin that adds 14 opinionated rules (`gajaguar-*` messages) plus a
smoke checker, encoding review preferences that ruff's `lint.select = ["ALL"]`
doesn't cover: no docstrings, mandatory AAA section markers in tests, `Final`
on module constants, and so on. The plugin self-lints this repository:
`make pylint` runs its rules against `src` and `tests`, so a regression in the
plugin fails the same gate it defines.

## Command surface

- Run the `Makefile` targets (`make check`, `make fix`, `make test`, ...)
  instead of the underlying tools, so the agent and CI use the same options.
  `make help` lists them.
- Give every new target a `##` help line; `make help` prints it and
  `make help-check` fails on a target without one.
- Scope a target to specific files with `FILES=`, for example
  `make lint FILES="src/pylint_gajaguar/scopes.py"` or
  `make pytest FILES="tests/checkers/test_scopes.py::test_name -x"`.
- Override the AAA section markers without touching config with
  `TEST_SECTION_MARKERS="Given When Then" make pylint`.
- Treat `check*` targets as read-only (they exit non-zero on problems and form
  the CI gate) and `fix*` targets as mutating files in place.

## Gate

- `make check` and `make test` MUST pass before any commit.
- Run `make fix` first for findings it can repair, then edit by hand.

## Commits and branches

- Write commit messages as
  [Conventional Commits](https://www.conventionalcommits.org/) and branch
  names as [Conventional Branch](https://conventionalbranch.org/)
  (`<type>/<description>`, e.g. `feat/add-checker`,
  `fix/frozenset-false-positive`). A pre-commit hook and
  `make commits-check` enforce both; see
  [`docs/conventions/commits-check.md`](docs/conventions/commits-check.md).
- Name a documentation or dependency branch `chore/...`: a branch type is not
  a commit type, and `docs/` is not one.
- Scope checker and checker-test edits to one checker per change.

## Pull requests

Once a pull request is open, the agent MUST:

1. Wait for CI; while it fails, fix the cause, push to the same branch and
   wait again until it passes.
2. Squash-merge a pull request with exactly one commit and use a regular merge
   commit otherwise (`gh pr view --json commits` gives the count).
3. Delete the branch on the remote and locally.
4. Switch back to the base branch, pull it and run `git fetch --prune`.

## Documentation

- Write documentation as an OKF bundle of atomic notes under `docs/`: one
  Markdown concept per file, with YAML frontmatter (`type`, `title`,
  `description`).
- Add a new note to its directory's `index.md` and, by file name, to
  [`docs/log.md`](docs/log.md); `make docs-lint` fails on a missing field or a
  broken link.
- Write a note only when it explains something a reader cannot already get
  from `make help`, a linter's own message, or the configuration it comes
  from.

## Dependencies

- Add a new tool to the ecosystem manager that owns it; use `mise.toml` only
  for a tool that bootstraps an ecosystem or has no manager in this
  repository. See
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

- The distribution is `pylint-gajaguar` and the single top-level package is
  `pylint_gajaguar`: hatchling finds `src/pylint_gajaguar/` from the project
  name and installs it without the `src/` prefix. In-repo imports read
  `from pylint_gajaguar.foo import Bar`, not `from src.pylint_gajaguar.foo
  import Bar`.
- Keep pylint's plugin loading and messages-control `enable` list in
  `pyproject.toml` (`[tool.pylint.main]`, `[tool.pylint."messages
  control"]`), not in CLI flags, so `mk/python.mk`'s `pylint` target and the
  pre-commit `pylint` hook stay in sync by construction.
- Register every checker under the single name `gajaguar`, so
  `enable = ["gajaguar"]` turns on every rule, including future ones. The
  `gajaguar-*` names are message symbols, not checker names.

## Adding a checker

- Follow the three-file procedure in
  [`CONTRIBUTING.md`](CONTRIBUTING.md#adding-a-checker): the checker module,
  its registration in `_register.py`, and its test.
- Set `name = "gajaguar"` on the checker, with a unique `gajaguar-...` message
  symbol and a unique message code.
- Derive the expected message span in a test from `node_position` (a node's
  header position, not its full body span): pylint reports
  `FunctionDef`/`ClassDef` messages against `node.position`.
- Run `make check` and `make test` afterwards: `make check` runs the new rule
  against the plugin's own source, so a rule its own code violates surfaces
  immediately.

## Test scoping

- Expect `gajaguar-test-*` checkers to activate only on files whose stem
  starts with `test_`, ends with `_test`, or whose parent directory is named
  `test`/`tests` (`scopes.is_test_file`), and only on `test_*` functions
  within them (`scopes.is_test_function`).
- Expect the other checkers (`gajaguar-no-docstrings`,
  `gajaguar-module-const-naming`, `gajaguar-require-final`, ...) to apply
  everywhere.

## Python

- Write no docstrings on functions, methods or classes; add a comment only
  where the *why* is not obvious from the code. `gajaguar-no-docstrings`
  fails `make check` on any docstring, and pylint has no autofix for it, so
  remove them by hand.
- Enable the plugin with `enable = ["gajaguar"]` in `pyproject.toml`'s
  `[tool.pylint."messages control"]`, not with a list of rules, so a rule
  added by a `pylint-gajaguar` upgrade runs without a config change.
- Run `make install` when `make conventional-git-latest` (part of
  `make check`) reports that `conventional-git` is behind PyPI.
- Keep `pyproject.toml` to settings that differ from the tool's default, and
  keep a `lint.per-file-ignores` entry only while it matches a current
  violation; see
  [`docs/python/pyproject-defaults.md`](docs/python/pyproject-defaults.md).
- Use absolute imports (`gajaguar-no-relative-imports`):
  `from pylint_gajaguar.foo import Bar`, not `from .foo import Bar`.
- Name module-level constants in `SCREAMING_SNAKE_CASE`
  (`gajaguar-module-const-naming`), annotate them `Final`
  (`gajaguar-require-final`) and write module-level set constants as
  `frozenset(...)` (`gajaguar-frozenset-constant`).
- Disable a rule inline or with `disable-next`, never with a standalone
  `# pylint: disable=` (`gajaguar-no-file-level-disable`).
- Keep imports at module top (`gajaguar-no-inline-imports`).
- Use `contextlib.suppress(...)` over `try/except/pass`
  (`gajaguar-use-contextlib-suppress`).
- Write test bodies with exactly the configured AAA section markers (default
  `# Arrange` / `# Act` / `# Assert`) as comments, no blank lines and no extra
  comments (`gajaguar-test-aaa-markers`, `gajaguar-test-no-blank-lines`,
  `gajaguar-test-no-extra-comments`). Treat `gajaguar-test-partial-assertion`
  and `gajaguar-test-name-implementation-detail` as advisory heuristics with a
  known false-positive rate, not hard gates.
- Justify a ruff ignore with an inline `# noqa: <rule>`. mypy runs `strict`
  and pyright is clean on `src` (tests are excluded from both).
