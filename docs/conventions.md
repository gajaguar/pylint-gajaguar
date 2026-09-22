# Conventions

## README structure

A README is written for a developer who needs to get productive, not as a
table of contents to fill in. Every project built from
[project-template](https://github.com/gajaguar/project-template) follows the
same outer shape, but the sections in the middle are whatever *this* project
actually has. Do not copy sections from another project's README if they do
not apply here:

1. **Title**, then a badge row: CI, license, and topics (generate the topics
   badge from the repo's actual GitHub topics with `gh repo edit --add-topic`
   rather than hand-picking tags that can drift out of sync), then a one-line
   description.
2. **`## About`** — the problem the project solves and its role in the wider
   system.
3. **`## Key features`** — capabilities that help a developer decide whether
   the project fits their needs.
4. **`## Requirements`** — what has to exist before anything else works.
5. **`## Usage`** — the smallest command sequence that gets something done.
6. **Getting started** — installation or project creation steps, when they are
   distinct from usage.
7. Whatever reference sections this project's own components or decisions
   warrant, including architecture diagrams, cross-linked with anchors such
   as `[Containers](#containers)` rather than repeated prose, and tables for
   anything enumerable.
8. **`## Platform notes`** — non-obvious behavior forced by the underlying
   platform (GitHub, the OS, a provider), not by the project's own design.
9. **`## Contributing`** — the shortest path to a valid contribution, with
   detailed rules linked from the README.
10. **`## Open items`** — known gaps or unverified assumptions, stated plainly.
    Omit the section rather than write "none"; an absent section already says
    that.
11. **`## License`** — the license governing use, modification, and
    distribution.

Skip a section if the project genuinely has nothing to put in it; do not pad
it with filler to preserve the shape. Add a table of contents when the README
is longer than 100 lines or has enough reference sections to make navigation
difficult.

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
for example `make md-lint FILES="README.md"`.

## Commits and branches

- Commit messages follow
  [Conventional Commits](https://www.conventionalcommits.org/); branch names
  follow [Conventional Branch](https://conventional-branch.github.io/).
- Scope checker and checker-test edits to one checker at a time so
  reviews stay focused.
