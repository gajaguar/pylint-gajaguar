# Contributing

Thanks for considering a contribution. Bug reports, feature ideas,
documentation fixes, and code are all welcome.

## Ways to contribute

- Report a bug or propose a feature by opening a GitHub issue. For a bug,
  include the steps to reproduce it and what you expected to happen.
- Fix or extend documentation under `docs/`.
- Submit a pull request for a bug fix or a new rule. For anything larger
  than a small fix, open an issue first so the approach can be agreed before
  you invest time in it.

## Set up

Install the toolchain and dependencies as described in the
[README](README.md#requirements), then:

```bash
make install
```

Run `make help` for the full list of targets.

## Adding a rule

A new rule touches three places. Keep them in this order:

1. Create `src/<name>.rs` with `pub const CODE: &str = "GAJ0nn"`, a
   `pub fn rule() -> Rule` (code, name, message, and `.pylint(msg-id, symbol)`
   for the alias) and a `pub fn visit(node, cx)` that reports through
   `cx.report`. `src/no_relative_imports.rs` is the smallest example.
2. Register it in `src/lib.rs`: add `mod <name>;`, `.rule(<name>::rule())` in
   `info` and `<name>::visit(node, cx)` in `visit`.
3. Add `tests/fixtures/GAJ0nn/` with the Python inputs and an `expected` file of
   `path<TAB>line<TAB>message` rows, one per finding. A test-scoped rule needs
   inputs named `test_*.py`. An option goes in `options.json`; a second variant
   of the same rule goes in `GAJ0nn-<suffix>/`.

`make test` compares the findings of the built plugin with each `expected`
file. Keep each rule in its own pull request.

## Conventions

- Justify a clippy allow with a comment next to it; `make clippy` treats
  warnings as errors.
- Do not add a dependency for a few lines; `make deny` audits licenses and
  advisories.

## Before opening a pull request

Run the gate and the tests (the latter needs `ferrolint` on `PATH`, see the
[README](README.md#develop-this-repository)); both MUST pass:

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
  `<type>/<description>`, for example `feat/add-rule` or
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
