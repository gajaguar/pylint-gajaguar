# Conventions

## Command convention: `check` vs `fix`

Targets are split by whether they mutate files:

| Umbrella            | Behavior                                                             |
| ------------------- | -------------------------------------------------------------------- |
| `check` (read-only) | Reports problems, exits non-zero, never writes. This is the CI gate. |
| `fix` (writable)    | Mutates files in place.                                              |

`check` runs `makefile-lint`, `md-lint`, `spell`, plus the language
targets (`lint`, `format-check`, `typecheck`, `pylint`) contributed by
`mk/python.mk`.

## Scoping with `FILES=`

Most targets accept `FILES="..."` to limit scope to specific paths or globs,
e.g. `make md-lint FILES="README.md"`.

## Commits and branches

- Commit messages follow
  [Conventional Commits](https://www.conventionalcommits.org/); branch names
  follow [Conventional Branch](https://conventional-branch.github.io/).
- Scope checker and checker-test edits to one checker at a time so
  reviews stay focused.
