# Contributing

## Setup

Run `make install` to sync the Python virtualenv, install the Node toolchain
(markdownlint-cli2, cspell) via pnpm, and register the pre-commit hook.

The Makefile splits every quality task by whether it mutates files: `check*`
targets are read-only and exit non-zero on problems, `fix*` targets rewrite
files in place. Most targets accept `FILES="path/glob"` to scope the run.

See [`docs/toolchain.md`](docs/toolchain.md) for the full toolchain list and
[`docs/conventions.md`](docs/conventions.md) for the `check` vs `fix`
convention. Python-layer specifics (docstring policy, interpreter source,
pylint configuration) live in [`docs/python.md`](docs/python.md).

## Adding a checker

A new checker touches three files. Keep them in this order:

1. Create the checker module in `src/checkers/<name>.py`. Subclass
   `pylint.checkers.BaseChecker`, set a unique `name = "app-..."` and a unique
   message code, and group test-related checkers around the helpers in
   `src/checkers/scopes.py`.
2. Register the class in `src/checkers/_register.py`. Import the new checker
   and add `linter.register_checker(NewChecker(linter))` to `register`. The
   order is cosmetic but stable.
3. Add `tests/checkers/test_<name>.py`. Use `pylint.testutils.CheckerTestCase`
   and the builders in `tests/conftest.py` (`build_module_from_source`,
   `build_test_module_from_source`, `node_position`). When the checker is
   test-scoped, build the module through `build_test_module_from_source` so
   the filename starts with `test_`.

After the three-file edit, run `make check` and `make test` from the repo
root. `make check` runs the new rule against itself via `make pylint`, so
introductions that violate the rule will surface there first.

## Conventions

- No docstrings. Use comments only when the *why* isn't obvious from the
  code; `app-no-docstrings` fails `make check` on any.
- Absolute imports only. `app-no-relative-imports` enforces this.
- Linting: ruff with `lint.select = ["ALL"]`. Justified ignores are written
  with `# noqa: <rule>` next to the line.
- Typing: mypy in `strict` mode and pyright clean. Use `TYPE_CHECKING` for
  third-party and pylint imports.
- Commits follow Conventional Commits.
