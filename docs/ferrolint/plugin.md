---
type: reference
title: ferrolint plugin
description: The ferrolint/ crate ports the gajaguar-* rules to a single WASM plugin; how it is built, tested against the Python checkers and where it differs.
tags: [ferrolint]
status: stable
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
| `GAJ006` | `W9006` | `gajaguar-no-file-level-disable`           |
| `GAJ008` | `W9008` | `gajaguar-no-inline-imports`               |
| `GAJ009` | `W9009` | `gajaguar-no-relative-imports`             |
| `GAJ012` | `W9012` | `gajaguar-use-contextlib-suppress`         |
| `GAJ013` | `W9013` | `gajaguar-frozenset-constant`              |
| `GAJ014` | `C9014` | `gajaguar-require-final`                   |
| `GAJ015` | `W9015` | `gajaguar-test-no-extra-comments`          |
| `GAJ016` | `W9016` | `gajaguar-test-partial-assertion`          |
| `GAJ017` | `W9017` | `gajaguar-test-name-implementation-detail` |

The code is `GAJ0` plus the last two digits of the Pylint msg-id.

## Build and test

* `make ferrolint-build` builds `ferrolint/target/wasm32-wasip2/release/pylint_gajaguar_ferrolint.wasm`.
  `make ferrolint-sha256` builds it and prints the file's sha256, the value
  for `sha256` in `ferrolint.toml`.
* `make ferrolint-test FERROLINT=<binary>` builds it, then lints every
  `ferrolint/fixtures/<CODE>/` directory with ferrolint (selecting only that
  rule) and with Pylint, and fails when the sets of file, line and message
  differ. `CODES="GAJ009"` limits the run. Pylint is the oracle, so a fixture
  needs no hand-written expectation. A directory may carry a suffix
  (`GAJ015-markers`) and an `options.json` of option names to text, which
  ferrolint reads as the plugin's options and Pylint as `--name=value`.
* `make ferrolint-clippy` and `make ferrolint-fmt` lint and format the crate.

None of these targets is part of `make check` or `make test`: building needs
the SDK from a private git repository and the fixtures need a ferrolint
binary. The `ferrolint` workflow (`.github/workflows/ferrolint.yml`) runs them
on a change to the crate, to the Python checkers or to the fixture runner. It
reads an SSH deploy key for the private repository from the
`FERROLINT_DEPLOY_KEY` secret and installs ferrolint at the tag in its
`FERROLINT_TAG`.

## Getting the plugin

There is no published `.wasm`: build it from this repository. It needs a Rust
toolchain with the `wasm32-wasip2` target (`rustup target add wasm32-wasip2`)
and SSH access to the ferrolint repository, where the SDK lives.

```bash
make ferrolint-sha256
```

builds the plugin and prints its sha256. The hash can change with the toolchain,
so compute it on the machine that will load the file and put both in
`ferrolint.toml`; ferrolint refuses a plugin whose hash differs.

## Differences from the Python checkers

* `test-section-markers` is a comma-separated list read by
  `gajaguar-test-aaa-markers` and `gajaguar-test-no-extra-comments`: set it in
  the `options` table of the plugin's `[[plugins]]` entry, which no other
  plugin sees, or as a configuration option (`[options]` in `ferrolint.toml`,
  or the Pylint file); the plugin's own value wins. Without either, the markers
  are `Arrange, Act, Assert`. The `TEST_SECTION_MARKERS` environment variable
  is not visible to a plugin.

  ```toml
  [[plugins]]
  path = "pylint_gajaguar_ferrolint.wasm"
  sha256 = "…"
  options = { test-section-markers = "Given, When, Then" }
  ```

* A file counts as a test file by its path as ferrolint reports it, relative
  to the working directory; Pylint checks the absolute path. The two differ
  only when the working directory itself is, or sits below, a directory named
  `test` or `tests`: run ferrolint from the project root. The fixtures cover
  `test/` and `tests/` directories inside the working directory, and names
  that only look like one (`contests/`, `pkg_test/`).
* `gajaguar-no-file-level-disable` finds a comment's line by the comment
  ranges the SDK gives, not by tokens. Like Pylint it counts the closing line
  of a multi-line string as standalone, and a string implicitly concatenated
  after it on that line as code; a closing f-string counts as code too. It
  finds the literals by scanning the text, skipping the replacement fields of
  an f-string whole, so quotes nested in them (Python 3.12+) are handled.
* Reported ranges are ferrolint's (the whole statement for most rules); only
  the line and the message are compared with Pylint.
