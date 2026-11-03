# pylint-gajaguar

[![CI](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/ci.yml/badge.svg)](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pylint-gajaguar.svg)](https://pypi.org/project/pylint-gajaguar/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Topics](https://img.shields.io/badge/topics-ferrolint%20%7C%20pylint%20%7C%20code--quality%20%7C%20lint%20%7C%20linter%20%7C%20python%20%7C%20static--analysis-informational)](https://github.com/gajaguar/pylint-gajaguar)

Opinionated lint rules that encode review preferences beyond ruff, as a
[ferrolint](https://github.com/gajaguar/ferrolint) plugin.

> **From 3.0.0 the package only works with ferrolint.** It no longer loads in
> Pylint. Pin `pylint-gajaguar==2.0.3`, the last version for Pylint, to keep
> using it there.

## Table of Contents

- [About](#about)
- [Key features](#key-features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Getting started](#getting-started)
- [Architecture](#architecture)
- [Built with](#built-with)
- [Configuration](#configuration)
  - [Rule reference](#rule-reference)
  - [Options](#options)
  - [Test scoping](#test-scoping)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## About

Ruff with `lint.select = ["ALL"]` covers lint hygiene but leaves
review-time preferences unenforced: no docstrings on functions, mandatory
AAA section markers inside tests, `Final` annotations on module-level
constants, and similar project-specific rules. Restating these in code
review is repetitive and lossy.

This plugin encodes those preferences as 14 ferrolint rules. Each keeps the
Pylint msg-id and symbol it had in 2.0.3 as an alias.

## Key features

- **14 rules**: docstrings, AAA test markers, blank-line discipline, imports,
  naming, `Final` annotations, `frozenset` constants, and
  `contextlib.suppress`.
- **Test-scoped rules**: the `gajaguar-test-*` rules apply only to files named
  `test_*.py` or `*_test.py`, or under a directory named `test` or `tests`.
- **Configurable section markers**: tune the AAA markers with the
  `test-section-markers` option.
- **No Python dependencies**: the wheel carries one WASM component, built from
  the Rust crate in this repository.

## Requirements

[ferrolint](https://github.com/gajaguar/ferrolint) 1.1.0 or later. To build
from source: Rust with the `wasm32-wasip2` target, [uv](https://docs.astral.sh/uv/)
and, for the Markdown lint and spell targets, [pnpm](https://pnpm.io/).

## Usage

Install the package into the virtual environment that ferrolint reads:

```bash
uv pip install pylint-gajaguar
```

ferrolint finds the plugin only through `VIRTUAL_ENV`, and loads it only when
`load-plugins` names it. In `pyproject.toml`:

```toml
[tool.pylint.main]
load-plugins = ["pylint_gajaguar"]
```

Then run `ferrolint` in the project. Every rule is on; ferrolint does not read
the Pylint checker name, so `enable = ["gajaguar"]` selects nothing. Narrow the
set with `select` and `ignore` in `ferrolint.toml`, for example
`ignore = ["GAJ016", "GAJ017"]` to drop the two advisory rules.

See [ferrolint plugin](docs/ferrolint/plugin.md) for the codes, how the plugin
is built and tested, and where it differs from 2.0.3.

## Getting started

### Use in another project

Follow [Usage](#usage).

### Develop this repository

```bash
git clone https://github.com/gajaguar/pylint-gajaguar.git
cd pylint-gajaguar
make install
make help
```

`make check` is the read-only gate, `make fix` applies safe fixes and
`make test` runs the plugin over the fixtures with `ferrolint` on `PATH`
(`uv tool install ferrolint==1.1.0`). `make wheel` builds the wheel into
`dist/`.

## Architecture

```text
ferrolint (load-plugins = ["pylint_gajaguar"])
  -> ferrolint.plugins entry point -> python/pylint_gajaguar/plugin.wasm
    -> src/lib.rs: registers each rule module (one file per rule)
tests/fixtures/<CODE>*/ -> *.py inputs + expected findings per rule
```

The crate builds to `target/wasm32-wasip2/release/pylint_gajaguar.wasm`;
`make plugin` copies it into the `pylint_gajaguar` package, which hatchling
packs into a `py3-none-any` wheel with the `ferrolint.plugins` entry point.

## Built with

- [Rust](https://www.rust-lang.org/) and the
  [ferrolint plugin SDK](https://crates.io/crates/ferrolint-plugin-sdk) — the
  rules
- [hatchling](https://hatch.pypa.io/) and [uv](https://docs.astral.sh/uv/) —
  the wheel
- [clippy](https://doc.rust-lang.org/clippy/), rustfmt and
  [cargo-deny](https://embarkstudios.github.io/cargo-deny/) — Rust checks
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
  and [cspell](https://cspell.org/) via pnpm (dev-only) — Markdown lint
  and spell
- [pre-commit](https://pre-commit.com/) — git hook runner

## Configuration

### Rule reference

| Code     | Rule (`name`)                              | Pylint  | Enforces                                                        |
| -------- | ------------------------------------------ | ------- | --------------------------------------------------------------- |
| `GAJ001` | `gajaguar-no-docstrings`                   | `W9001` | No docstrings on functions, methods, or classes (use comments)  |
| `GAJ002` | `gajaguar-test-aaa-markers`                | `W9002` | `test_*` bodies contain `# Arrange`, `# Act`, `# Assert`        |
| `GAJ003` | `gajaguar-test-no-blank-lines`             | `W9003` | No blank lines inside test method bodies                        |
| `GAJ004` | `gajaguar-unused-arg-use-del`              | `W9004` | Use `del arg` at body top, not a `_`-prefixed arg               |
| `GAJ005` | `gajaguar-module-const-naming`             | `C9005` | Module-level names are `SCREAMING_SNAKE_CASE`                   |
| `GAJ006` | `gajaguar-no-file-level-disable`           | `W9006` | No standalone `# pylint: disable=`; use inline / `disable-next` |
| `GAJ008` | `gajaguar-no-inline-imports`               | `W9008` | Imports at module top, not inside functions                     |
| `GAJ009` | `gajaguar-no-relative-imports`             | `W9009` | Absolute imports only                                           |
| `GAJ012` | `gajaguar-use-contextlib-suppress`         | `W9012` | `contextlib.suppress(...)` over `try/except/pass`               |
| `GAJ013` | `gajaguar-frozenset-constant`              | `W9013` | Module-level set constants use `frozenset(...)`                 |
| `GAJ014` | `gajaguar-require-final`                   | `C9014` | Module-level constants carry a `Final` annotation               |
| `GAJ015` | `gajaguar-test-no-extra-comments`          | `W9015` | Test bodies carry only the configured section markers           |
| `GAJ016` | `gajaguar-test-partial-assertion`          | `W9016` | Field assertions without a whole-object assertion (advisory)    |
| `GAJ017` | `gajaguar-test-name-implementation-detail` | `W9017` | Test names naming mocks, patches, internals (advisory)          |

`gajaguar-test-partial-assertion` and `gajaguar-test-name-implementation-detail`
use heuristics with a measurable false-positive rate; treat their output
as advisory, not a hard gate.

### Options

| Option                 | Type | Default              | Description                                                                |
| ---------------------- | ---- | -------------------- | -------------------------------------------------------------------------- |
| `test-section-markers` | csv  | `Arrange,Act,Assert` | Section names a test body must carry, in order, without the `#` mark.      |

Set it as a configuration option (`[options]` in `ferrolint.toml`), or in the
`options` table of a `[[plugins]]` entry. The `TEST_SECTION_MARKERS`
environment variable of 2.0.3 is gone. See
[ferrolint plugin](docs/ferrolint/plugin.md#differences-from-203-under-pylint).

### Test scoping

The `gajaguar-test-*` rules activate only on files matching one of these:

- Stem starts with `test_` (e.g. `test_module.py`)
- Stem ends with `_test` (e.g. `module_test.py`)
- Any parent directory is named `test` or `tests`

Files outside those paths are skipped entirely. Function-scoping applies
on top: a `test_*` function inside a test file is checked; a `helper`
function in the same file is not. Run ferrolint from the project root.

## Contributing

Read [CONTRIBUTING.md][contributing] for the local setup, the conventions
and the procedure for adding a rule.

## Security

Report vulnerabilities privately by email to <dev@gajaguar.com>. Do not
open a public issue, pull request, or discussion.

See [SECURITY.md][security] for supported versions and the reporting
process.

## License

Distributed under the MIT License. See [LICENSE][license] for the full
text.

[contributing]: https://github.com/gajaguar/pylint-gajaguar/blob/main/CONTRIBUTING.md
[security]: https://github.com/gajaguar/pylint-gajaguar/blob/main/SECURITY.md
[license]: https://github.com/gajaguar/pylint-gajaguar/blob/main/LICENSE
