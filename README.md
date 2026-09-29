# Pylint Plugin

[![CI](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/ci.yml/badge.svg)](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/ci.yml)
[![Python CI](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/python.yml/badge.svg?branch=main)](https://github.com/gajaguar/pylint-gajaguar/actions/workflows/python.yml)
[![ruff](https://img.shields.io/badge/ruff-checked-orange?style=flat-square&logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)
[![pylint](https://img.shields.io/badge/pylint-checked-428f7f?style=flat-square)](https://pylint.pycqa.org/)
[![mypy](https://img.shields.io/badge/mypy-checked-blue?style=flat-square)](http://mypy-lang.org/)
[![PyPI](https://img.shields.io/pypi/v/pylint-gajaguar?style=flat-square)](https://pypi.org/project/pylint-gajaguar/)
[![python](https://img.shields.io/badge/python->=3.14-blue?style=flat-square)](https://docs.python.org/3.14/)
[![Topics](https://img.shields.io/badge/topics-pylint%20%7C%20pylint--plugin-informational)](https://github.com/gajaguar/pylint-gajaguar)
[![license](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

Opinionated pylint checkers that encode review preferences beyond ruff,
self-linting this repository.

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
  - [Make variables](#make-variables)
- [Contributing](#contributing)
- [Security](#security)
- [Open items](#open-items)
- [License](#license)

## About

Ruff with `lint.select = ["ALL"]` covers lint hygiene but leaves
review-time preferences unenforced: no docstrings on functions, mandatory
AAA section markers inside tests, `Final` annotations on module-level
constants, and similar project-specific rules. Restating these in code
review is repetitive and lossy.

This plugin encodes those preferences as 14 pylint checkers and runs them
against its own source tree. `make pylint` self-lints the repository with
the same rules, so a regression in the codebase fails the same gate that
defines the rule.

## Key features

- **14 enforced checkers**: docstrings, AAA test markers, blank-line
  discipline, imports, naming, `Final` annotations, `frozenset`
  constants, and `contextlib.suppress`.
- **Test-scoped rules**: the `gajaguar-test-*` checkers activate only on files
  under `tests/`, files matching `test_*.py` or `*_test.py`, or any parent
  named `test` or `tests`. Production code paths stay unaffected.
- **Configurable section markers**: tune the AAA markers via pylint
  option or environment variable without editing the plugin source.
- **One runtime dependency**: the wheel requires only `pylint`
  (`pylint>=4.0`).
- **Self-linting**: the plugin runs against itself in CI and in
  pre-commit; a rule violation fails the same gate that defines it.

## Requirements

Python 3.14 or higher — the package declares `requires-python = ">=3.14"`.
Install [uv](https://docs.astral.sh/uv/) for dependency management and
virtual environments. Install [pnpm](https://pnpm.io/) (or another Node
package manager) only if you plan to run the Markdown lint and spell
targets.

## Usage

Run pylint with the plugin against your source tree:

```bash
uv run pylint --load-plugins=pylint_gajaguar \
  --disable=all --enable=gajaguar src tests
```

The `pylint_gajaguar` argument is the module the wheel installs (see
[Architecture](#architecture)). The `--disable=all` flag is
deliberate: pylint's built-in rules overlap with ruff (line length,
import placement), and `missing-module-docstring` conflicts with
`gajaguar-no-docstrings`. `--enable=gajaguar` selects only the plugin's own
rules: every checker registers under the single name `gajaguar`, so rules
added in a later release are enabled without touching your configuration.

To run a subset, enable rules by message name instead, for example
`--enable=gajaguar-no-docstrings,gajaguar-require-final`.

For the local development loop in this repository:

```bash
make check   # read-only gate: lint, format, mypy, pyright, md-lint, spell, pylint
make fix     # apply safe auto-fixes
make test    # run the test suite
make help    # list every target
```

Scope a target to specific files:

```bash
make lint FILES="src/pylint_gajaguar/scopes.py"
make pylint FILES="src"
```

Override the AAA section markers without editing config:

```bash
TEST_SECTION_MARKERS="Given When Then" make pylint
```

## Getting started

### Use in another project

Install the plugin from [PyPI](https://pypi.org/project/pylint-gajaguar/)
as a dev dependency:

```bash
uv add --dev pylint-gajaguar
```

or with pip:

```bash
pip install pylint-gajaguar
```

Then run pylint with the plugin loaded (see [Usage](#usage) for the
`--enable=gajaguar` command).

### Develop this repository

Clone the repository and install everything (toolchain, Python deps,
Node toolchain, git hook):

```bash
git clone https://github.com/gajaguar/pylint-gajaguar.git
cd pylint-gajaguar
make install
```

## Architecture

```mermaid
flowchart LR
  Run[pylint --load-plugins=pylint_gajaguar] --> Pkg[pylint_gajaguar.register]
  Pkg --> Def[pylint_gajaguar._register.register]
  Def --> Checks[Checker classes]
  Scopes[scopes.py: markers + scoping] --> Checks
  Checks --> Msgs[pylint messages]
```

The wheel ships a single top-level package, `pylint_gajaguar`:
`[tool.hatch.build.targets.wheel]` sets `sources = ["src"]`, so
`src/pylint_gajaguar/` installs as `pylint_gajaguar`. That is why
`--load-plugins=pylint_gajaguar` resolves: pylint calls `register` from the
package's `__init__.py`.

`pylint_gajaguar/__init__.py` re-exports `register` from `_register.py`,
which instantiates and registers each checker with the pylint linter.
`scopes.py` provides the shared section-marker option and test-scoping
helpers that the `gajaguar-test-*` checkers consume.

## Built with

- [uv](https://docs.astral.sh/uv/) — dependency management and venv
- [hatchling](https://hatch.pypa.io/) — build backend
- [pylint](https://pylint.pycqa.org/) /
  [astroid](https://github.com/PyCQA/astroid) — checker host runtime
- [ruff](https://docs.astral.sh/ruff/) — lint and format
  (`lint.select = ["ALL"]`)
- [mypy](https://mypy-lang.org/) +
  [pyright](https://microsoft.github.io/pyright/) — strict static type
  checking
- [pytest](https://docs.pytest.org/) — test runner
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
  and [cspell](https://cspell.org/) via pnpm (dev-only) — Markdown lint
  and spell
- [pre-commit](https://pre-commit.com/) — git hook runner

## Configuration

### Rule reference

`gajaguar-smoke` registers with pylint but carries no messages; it exists to
verify the registration wiring. The remaining 14 rules each carry a
message code and report violations.

| Rule (`name`)                              | Code  | Enforces                                                        |
| ------------------------------------------ | ----- | --------------------------------------------------------------- |
| `gajaguar-no-docstrings`                   | W9001 | No docstrings on functions, methods, or classes (use comments)  |
| `gajaguar-test-aaa-markers`                | W9002 | `test_*` bodies contain `# Arrange`, `# Act`, `# Assert`        |
| `gajaguar-test-no-blank-lines`             | W9003 | No blank lines inside test method bodies                        |
| `gajaguar-unused-arg-use-del`              | W9004 | Use `del arg` at body top, not a `_`-prefixed arg               |
| `gajaguar-module-const-naming`             | C9005 | Module-level names are `SCREAMING_SNAKE_CASE`                   |
| `gajaguar-no-file-level-disable`           | W9006 | No standalone `# pylint: disable=`; use inline / `disable-next` |
| `gajaguar-no-inline-imports`               | W9008 | Imports at module top, not inside functions                     |
| `gajaguar-no-relative-imports`             | W9009 | Absolute imports only                                           |
| `gajaguar-use-contextlib-suppress`         | W9012 | `contextlib.suppress(...)` over `try/except/pass`               |
| `gajaguar-frozenset-constant`              | W9013 | Module-level set constants use `frozenset(...)`                 |
| `gajaguar-require-final`                   | C9014 | Module-level constants carry a `Final` annotation               |
| `gajaguar-test-no-extra-comments`          | W9015 | Test bodies carry only the configured section markers           |
| `gajaguar-test-partial-assertion`          | W9016 | Field assertions without a whole-object assertion (advisory)    |
| `gajaguar-test-name-implementation-detail` | W9017 | Test names naming mocks, patches, internals (advisory)          |

`gajaguar-test-partial-assertion` and `gajaguar-test-name-implementation-detail`
use heuristics with a measurable false-positive rate; treat their output
as advisory, not a hard gate.

### Options

| Option                   | Type    | Default              | Description                                                                               |
| ------------------------ | ------- | -------------------- | ----------------------------------------------------------------------------------------- |
| `--test-section-markers` | csv     | `Arrange,Act,Assert` | Section names a test body must carry, in order, without their leading `#` comment marker. |
| `TEST_SECTION_MARKERS`   | env var | (unset)              | Space-separated section names. Overrides `--test-section-markers` when set.               |

Resolution order: `TEST_SECTION_MARKERS` (env) →
`--test-section-markers` (linter config) → the default tuple. Set the
env var to experiment with markers without rewriting the linter config.

In `pyproject.toml` the option lives under the checker name:

```toml
[tool.pylint.gajaguar]
test-section-markers = ["Given", "When", "Then"]
```

### Test scoping

The `gajaguar-test-*` rules activate only on files matching one of these:

- Stem starts with `test_` (e.g. `test_module.py`)
- Stem ends with `_test` (e.g. `module_test.py`)
- Any parent directory is named `test` or `tests`

Files outside those paths are skipped entirely. Function-scoping applies
on top: a `test_*` function inside a test file is checked; a `helper`
function in the same file is not.

### Make variables

| Variable | Behavior         | Examples                                                                            |
| -------- | ---------------- | ----------------------------------------------------------------------------------- |
| `FILES`  | Scope by path    | `FILES="src/pylint_gajaguar/scopes.py"` or `FILES="src/pylint_gajaguar/*.py"`       |
| `check*` | Read-only gate   | `make check`, `make lint`, `make pylint`, `make mypy`, `make md-lint`, `make spell` |
| `fix*`   | Mutates in place | `make fix`, `make lint-fix`, `make format`, `make md-fix`                           |

## Contributing

Contributions optimize this plugin. Fork the repository, create a
feature branch, commit your change, push, and open a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the local setup, the
`check` vs `fix` convention, and the three-file procedure for adding a
new checker.

## Security

Report vulnerabilities privately by email to <dev@gajaguar.com>. Do not
open a public issue, pull request, or discussion.

See [SECURITY.md](SECURITY.md) for supported versions and the reporting
process.

## Open items

- Dynamic checker discovery to remove the three-file registration step.
- `CHANGELOG.md`.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for the full
text.
