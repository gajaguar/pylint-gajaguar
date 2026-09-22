# Python layer

## Docstring policy

This project does not use docstrings — use comments only where the *why*
isn't obvious from the code. The plugin's own `app-no-docstrings` (W9001)
checker fails `make check`/`make pylint` on any function, method, or class
that has one. pylint has no autofix for this, so docstrings must be
removed by hand.

## Interpreter source

`mise.toml` is the single source for the pinned Python version;
`.python-version` is intentionally absent (mise ignores it by default) to
avoid a second, silently divergent source of truth. `pyproject.toml`
forces `uv` to use the mise-provided interpreter instead of downloading
its own:

```toml
[tool.uv]
python-preference = "only-system"
python-downloads = "never"
```

## Pylint configuration

Pylint's plugin loading and disable list live in `pyproject.toml` under
`[tool.pylint.main].load-plugins` and
`[tool.pylint."messages control"].disable`. `mk/python.mk`'s `pylint`
target and the pre-commit `pylint` hook both invoke `uv run pylint`
without `--load-plugins=` or `--enable=` flags — the plugin's own checker
list stays in one place. See the
[README's rule reference](../README.md#configuration) for the full list
of `app-*` checkers.
