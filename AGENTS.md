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

A ferrolint plugin (Rust, built to WASM and shipped in a `py3-none-any` wheel)
that adds 14 opinionated rules (`GAJ001`..`GAJ017`, with the `gajaguar-*`
Pylint symbols as aliases), encoding review preferences that ruff's
`lint.select = ["ALL"]` doesn't cover: no docstrings, mandatory AAA section
markers in tests, `Final` on module constants, and so on. From 3.0.0 it works
only with ferrolint; 2.0.3 is the last version for Pylint.

## Command surface

- Run the `Makefile` targets (`make check`, `make fix`, `make test`, ...)
  instead of the underlying tools, so the agent and CI use the same options.
  `make help` lists them.
- Give every new target a `##` help line; `make help` prints it and
  `make help-check` fails on a target without one.
- Scope the fixture run with `CODES=`, for example
  `make ferrolint-test CODES="GAJ009"`, and pick the binary with
  `FERROLINT=<binary>`; `make fmt FILES="src/lib.rs"` limits rustfmt.
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

## Versioning and releases

- Decide every version bump, tag and release as
  [`docs/conventions/versioning.md`](docs/conventions/versioning.md) defines;
  it is the only place those rules live.

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
ferrolint (load-plugins = ["pylint_gajaguar"])
  -> ferrolint.plugins entry point -> python/pylint_gajaguar/plugin.wasm
    -> src/lib.rs: registers each rule module
tests/fixtures/<CODE>*/ -> *.py inputs + expected findings per rule
```

- The distribution is `pylint-gajaguar`, the Cargo package is `pylint-gajaguar`
  and the Python package that carries `plugin.wasm` is `pylint_gajaguar`. The
  entry point name `pylint_gajaguar` is what a project's `load-plugins` names.
- Describe the plugin in [`docs/ferrolint/plugin.md`](docs/ferrolint/plugin.md).

## Adding a rule

- Follow the three-step procedure in
  [`CONTRIBUTING.md`](CONTRIBUTING.md#adding-a-rule): the rule module in
  `src/`, its registration in `src/lib.rs`, and a `tests/fixtures/GAJ0nn/`
  directory with an `expected` file.
- Give the rule a unique `GAJ0nn` code and keep the Pylint msg-id and symbol
  as its alias.
- Treat `expected` as the oracle: it was frozen from the Pylint checkers of
  2.0.3. Change one only for a deliberate change of the rule's behavior.
- Run `make check` and `make test` afterwards.

## Test scoping

- Expect `GAJ002`, `GAJ003`, `GAJ015`, `GAJ016` and `GAJ017` (the
  `gajaguar-test-*` rules) to activate only on files whose stem starts with
  `test_`, ends with `_test`, or whose parent directory is named `test`/`tests`,
  and only on `test_*` functions within them.
- Expect the other rules to apply everywhere.

## Rust

- Pin the Rust version, its components and its compile targets in `mise.toml`
  only; never add `rust-toolchain.toml`, which mise does not read.
- Let `make fmt` decide `.rs` whitespace: rustfmt does not read
  `.editorconfig`.
- Set lint levels in `[lints]` in `Cargo.toml`, never as flags in `mk/rust.mk`.
- Pin `cargo-deny` in `mk/rust.mk` and install it with `cargo install`, not
  mise; `make deny` runs in `make check`.
- Depend on `ferrolint-plugin-sdk` from crates.io, pinned to `=1.1.0`: the SDK
  version is the plugin contract's version.
- Tag a minor or major bump with `make release-tag` after its pull request
  merges, as [`docs/conventions/versioning.md`](docs/conventions/versioning.md)
  describes; the target tags the base branch as `v<package.version>`, read
  from `Cargo.toml`. Keep `pyproject.toml`'s `version` equal to it: the
  `publish` workflow fails otherwise.
