# Contributing

Thanks for considering a contribution. Bug reports, feature ideas,
documentation fixes, and code are all welcome.

## Ways to contribute

- Report a bug or propose a feature by opening a GitHub issue. For a bug,
  include the steps to reproduce it and what you expected to happen.
- Fix or extend documentation under `docs/`.
- Submit a pull request for a bug fix or a new checker. For anything larger
  than a small fix, open an issue first so the approach can be agreed before
  you invest time in it.

## Set up

Install the toolchain and dependencies as described in the
[README](README.md#requirements), then:

```bash
make install
```

Run `make help` for the full list of targets.

## Adding a checker

A new checker touches three files. Keep them in this order:

1. Create the checker module in `src/pylint_gajaguar/<name>.py`. Subclass
   `pylint.checkers.BaseChecker`, set a unique `name = "gajaguar-..."` and a
   unique message code, and group test-related checkers around the helpers in
   `src/pylint_gajaguar/scopes.py`.
2. Register the class in `src/pylint_gajaguar/_register.py`. Import the new
   checker and add `linter.register_checker(NewChecker(linter))` to
   `register`. The order is cosmetic but stable.
3. Add `tests/checkers/test_<name>.py`. Use `pylint.testutils.CheckerTestCase`
   and the builders in `tests/conftest.py` (`build_module_from_source`,
   `build_test_module_from_source`, `node_position`). When the checker is
   test-scoped, build the module through `build_test_module_from_source` so
   the filename starts with `test_`.

Then enable the new rule in `pyproject.toml`'s
`[tool.pylint."messages control"].enable`; `make check` fails until you do.
It also runs the rule against the plugin's own source, so a change that
violates its own rule surfaces there first. Keep each checker in its own
pull request.

## Conventions

- No docstrings. Use comments only when the *why* isn't obvious from the
  code; `gajaguar-no-docstrings` fails `make check` on any.
- Absolute imports only; `gajaguar-no-relative-imports` enforces this.
- Justified ruff ignores are written with `# noqa: <rule>` next to the line.
- mypy runs in `strict` mode and pyright is clean. Use `TYPE_CHECKING` for
  third-party and pylint imports.

## Before opening a pull request

Run the gate and the tests; both MUST pass:

```bash
make check
make test
```

`make fix` applies the safe automatic fixes for what `make check` reports.
CI runs the same targets and blocks the merge when either fails.

## Commits and branches

- Commit messages follow
  [Conventional Commits](https://www.conventionalcommits.org/).
- Branch names follow
  [Conventional Branch](https://conventionalbranch.org/):
  `<type>/<description>`, for example `feat/add-checker` or
  `fix/frozenset-false-positive`. The branch type is one of `feat`, `fix`,
  `hotfix`, `release`, or `chore`; documentation work uses `chore/`.

A pre-commit hook and `make commits-check` enforce both; see
[`docs/conventions/commits-check.md`](docs/conventions/commits-check.md).

## Documentation

`docs/` is a bundle of atomic notes: one concept per file. A new note is
added to its directory's `index.md` and to [`docs/log.md`](docs/log.md) in
the same pull request. Read [`AGENTS.md`](AGENTS.md) for the rules that apply
to both people and coding agents working in this repository.

## License

By contributing, you agree that your contribution is licensed under the
project's license; see [LICENSE](LICENSE).
