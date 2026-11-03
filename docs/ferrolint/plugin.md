---
type: reference
title: ferrolint plugin
description: pylint-gajaguar 3.0.0 is a ferrolint WASM plugin; how to install, build and test it, and where it differs from 2.0.3 under Pylint.
tags: [ferrolint]
status: stable
---

# ferrolint plugin

pylint-gajaguar is a Rust crate built as one `cdylib` for `wasm32-wasip2` and
shipped in a `py3-none-any` wheel. From 3.0.0 it replaces the Pylint checkers:
2.0.3 is the last version that loads in Pylint, and 3.0.0 needs
[ferrolint](https://github.com/gajaguar/ferrolint) 1.1.0 or later. Each rule
keeps its Pylint msg-id and symbol as an alias, so `# pylint: disable=gajaguar-no-docstrings`
and `select = ["W9001"]` still work.

## Install

```bash
uv pip install pylint-gajaguar
```

ferrolint finds the plugin through the `ferrolint.plugins` entry point of the
virtual environment in `VIRTUAL_ENV`, and loads it only when `load-plugins`
names the entry point, `pylint_gajaguar`:

```toml
[tool.pylint.main]
load-plugins = ["pylint_gajaguar"]
```

Every rule is then on. ferrolint does not read the Pylint checker name, so
`enable = ["gajaguar"]` selects nothing; with `disable = ["all"]` the plugin
reports nothing. Narrow the set with `select` and `ignore` in `ferrolint.toml`.

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

* `make plugin-build` builds `target/wasm32-wasip2/release/pylint_gajaguar.wasm`.
  `make plugin` copies it to `python/pylint_gajaguar/plugin.wasm` and
  `make wheel` builds the wheel into `dist/`. `make ferrolint-sha256` prints the
  file's sha256, for a `[[plugins]]` entry outside pip.
* `make ferrolint-test` (part of `make test`) lints every `tests/fixtures/<CODE>/`
  directory with ferrolint, selecting only that rule, and fails when the set of
  file, line and message differs from the directory's `expected` file. The
  `expected` files were frozen from the Pylint checkers of 2.0.3, so they are
  the oracle; regenerate one only for a deliberate change. `CODES="GAJ009"`
  limits the run and `FERROLINT=<binary>` picks the binary (default `ferrolint`
  on `PATH`). A directory may carry a suffix (`GAJ015-markers`) and an
  `options.json` of option names to text, which ferrolint reads as the plugin's
  options.
* `make clippy`, `make fmt` and `make deny` lint, format and audit the crate;
  `make check` runs them.

The `rust` workflow (`.github/workflows/rust.yml`) runs `make check` and
`make test` with `uv tool install ferrolint==1.1.0`. A published release runs the
`publish` workflow, which builds the wheel and uploads it to PyPI.

## Differences from 2.0.3 under Pylint

* `test-section-markers` is a comma-separated list read by
  `gajaguar-test-aaa-markers` and `gajaguar-test-no-extra-comments`: set it in
  the `options` table of a `[[plugins]]` entry (a plugin loaded by path), which
  no other plugin sees, or as a configuration option (`[options]` in
  `ferrolint.toml`, or the Pylint file); the plugin's own value wins. Without
  either, the markers are `Arrange, Act, Assert`. The `TEST_SECTION_MARKERS`
  environment variable is not visible to a plugin.

  ```toml
  [[plugins]]
  path = "pylint_gajaguar.wasm"
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
