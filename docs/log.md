# Directory Update Log

## 2026-09-29

* **Change**: The pre-commit hooks and `CONVENTIONAL_GIT` now run
  `uvx conventional-git@latest`, the dev dependency requires
  `conventional-git>=1.1`, and the `dependabot/*` skip in
  `make commits-check` is gone: 1.1.0 accepts `dependabot/` and `renovate/`
  branch names itself. Updated
  [`conventions/commits-check.md`](conventions/commits-check.md).

## 2026-09-28

* **Addition**: Added PyPI Trusted Publishing under `release/`.
* **Restructure**: Replaced the flat `conventions.md`, `python.md` and
  `toolchain.md` with one note per concept under `conventions/`,
  `toolchain/` and `python/`, each listed in its directory `index.md`.
