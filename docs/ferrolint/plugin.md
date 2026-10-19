---
type: reference
title: ferrolint plugin
description: The ferrolint/ crate ports the gajaguar-* rules to a single WASM plugin; how it is built, tested against the Python checkers and where it differs.
tags: [ferrolint]
status: draft
---

# ferrolint plugin

`ferrolint/` is a Rust crate built as one `cdylib` for `wasm32-wasip2`. It
ports the `gajaguar-*` rules to a [ferrolint](https://github.com/gajaguar/ferrolint)
plugin. Each rule keeps its Pylint msg-id and symbol as an alias, so
`# pylint: disable=gajaguar-no-docstrings` and `select = ["W9001"]` still work.
The crate depends on the plugin SDK by git revision; `ferrolint/.cargo/config.toml`
makes cargo fetch it with the `git` CLI, so SSH credentials apply.

| Code     | Pylint  | Symbol                                     |
| :------- | :------ | :----------------------------------------- |
| `GAJ001` | `W9001` | `gajaguar-no-docstrings`                   |
| `GAJ002` | `W9002` | `gajaguar-test-aaa-markers`                |
| `GAJ003` | `W9003` | `gajaguar-test-no-blank-lines`             |
| `GAJ004` | `W9004` | `gajaguar-unused-arg-use-del`              |
| `GAJ005` | `C9005` | `gajaguar-module-const-naming`             |
| `GAJ008` | `W9008` | `gajaguar-no-inline-imports`               |
| `GAJ009` | `W9009` | `gajaguar-no-relative-imports`             |
| `GAJ012` | `W9012` | `gajaguar-use-contextlib-suppress`         |
| `GAJ013` | `W9013` | `gajaguar-frozenset-constant`              |
| `GAJ014` | `C9014` | `gajaguar-require-final`                   |
| `GAJ016` | `W9016` | `gajaguar-test-partial-assertion`          |
| `GAJ017` | `W9017` | `gajaguar-test-name-implementation-detail` |

The code is `GAJ0` plus the last two digits of the Pylint msg-id.

## Build and test

* `make ferrolint-build` builds `ferrolint/target/wasm32-wasip2/release/pylint_gajaguar_ferrolint.wasm`.
* `make ferrolint-test FERROLINT=<binary>` builds it, then lints every
  `ferrolint/fixtures/<CODE>/` directory with ferrolint (selecting only that
  rule) and with Pylint, and fails when the sets of file, line and message
  differ. `CODES="GAJ009"` limits the run. Pylint is the oracle, so a fixture
  needs no hand-written expectation.
* `make ferrolint-clippy` and `make ferrolint-fmt` lint and format the crate.

None of these targets is part of `make check` or `make test`: building needs
the SDK from a private git repository and the fixtures need a ferrolint
binary, neither of which CI has.

## Differences from the Python checkers

* `test-section-markers` is read as the `test-section-markers` option, a
  comma-separated list; the `TEST_SECTION_MARKERS` environment variable is
  not visible to a plugin.
* A file counts as a test file by its path as ferrolint reports it, relative
  to the working directory; Pylint checks the absolute path, so a parent
  directory named `tests` above the working directory no longer counts.
* `gajaguar-module-const-naming` does not see names bound by `match` patterns.
* Reported ranges are ferrolint's (the whole statement for most rules); only
  the line and the message are compared with Pylint.

## Not ported yet

`gajaguar-no-file-level-disable` and `gajaguar-test-no-extra-comments` are
missing: they need comments, which the AST does not carry.
