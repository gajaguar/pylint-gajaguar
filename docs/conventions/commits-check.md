---
type: rule
title: Enforcing commits and branches
description: A pre-commit hook checks the commit being written and the current branch name; make commits-check re-validates the whole range in CI.
tags: [git]
status: stable
---

# Enforcing commits and branches

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
and branch names follow [Conventional Branch](https://conventionalbranch.org/).
Two layers enforce both, via
[conventional-git](https://github.com/gajaguar/conventional-git):

* **Local**: `.pre-commit-config.yaml`'s `conventional-commit-msg` hook
  checks the message being written (`commit-msg` stage);
  `conventional-branch-name` checks the current branch name (`pre-commit`
  and `pre-push` stages).
* **CI**: `make commits-check` re-validates every commit in `$(BASE)..HEAD`
  and the branch name, since a local hook can be bypassed with
  `--no-verify`. It runs as part of `make check`.

Dependabot always names its branches `dependabot/<ecosystem>/<dependency>`,
which is not a Conventional Branch type, and its prefix can't be changed.
`make commits-check` therefore skips the branch-name check for
`dependabot/*` branches; the commit messages are still validated, and
`.github/dependabot.yml` sets their `ci`/`chore` prefixes.

`make commits-check` runs through `$(UV) run conventional-git` — the
project's own pinned dev dependency, already synced by `uv sync` — instead
of an ephemeral `uvx conventional-git` fetch, for a faster and
lockfile-reproducible CI run. The CI workflow checks out with
`fetch-depth: 0` and the pull request's head ref, so `$(BASE)`
(`origin/main`) and the branch name resolve correctly instead of hitting a
detached `HEAD`.
