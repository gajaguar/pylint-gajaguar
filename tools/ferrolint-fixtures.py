#!/usr/bin/env python3
"""Run the ferrolint plugin on the fixtures and compare with their expected findings.

ferrolint/fixtures/<CODE>*/*.py are linted with only the rule <CODE> selected.
The (file, line, message) triples must equal the tab-separated rows of the
directory's `expected` file, frozen from pylint-gajaguar 2.0.3 under Pylint.
A directory may add a suffix (GAJ015-markers) and an options.json, a flat
object of option name to text that ferrolint reads as the plugin's options.

Usage: ferrolint-fixtures.py WASM [CODE ...]
Environment: FERROLINT (the binary, default "ferrolint").
"""

import hashlib
import json
import os
import pathlib
import shlex
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"


def ferrolint(
    binary: str, wasm: pathlib.Path, code: str, directory: pathlib.Path, options: dict[str, str]
) -> set[tuple[str, int, str]]:
    digest = hashlib.sha256(wasm.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as tmp:
        config = pathlib.Path(tmp, "ferrolint.toml")
        table = ", ".join(f"{json.dumps(name)} = {json.dumps(value)}" for name, value in options.items())
        config.write_text(f'select = ["{code}"]\n[[plugins]]\npath = "{wasm}"\nsha256 = "{digest}"\noptions = {{ {table} }}\n')
        run = subprocess.run(
            [*shlex.split(binary), "-c", str(config), "--no-cache", "--format", "json", "."],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )
    if run.returncode not in {0, 1}:
        sys.exit(f"{code}: ferrolint failed\n{run.stderr}")
    found = json.loads(run.stdout)["diagnostics"]
    return {(d["path"], d["range"]["start"]["line"], d["message"]) for d in found}


def expected(directory: pathlib.Path) -> set[tuple[str, int, str]]:
    rows = (row.split("\t") for row in (directory / "expected").read_text().splitlines())
    return {(path, int(line), message) for path, line, message in rows}


def main() -> int:
    wasm = pathlib.Path(sys.argv[1]).resolve()
    wanted = set(sys.argv[2:])
    binary = os.environ.get("FERROLINT", "ferrolint")
    failed = False
    for directory in sorted(FIXTURES.iterdir()):
        code = directory.name[:6]
        if wanted and code not in wanted:
            continue
        settings = directory / "options.json"
        options = json.loads(settings.read_text()) if settings.exists() else {}
        ours = ferrolint(binary, wasm, code, directory, options)
        theirs = expected(directory)
        if not theirs:
            sys.exit(f"{directory.name}: expected is empty; the fixtures prove nothing")
        status = "ok" if ours == theirs else "DIFF"
        print(f"{directory.name}: {status} ({len(theirs)} findings)")  # noqa: T201
        if ours != theirs:
            failed = True
            for item in sorted(ours - theirs):
                print(f"  only ferrolint: {item}")  # noqa: T201
            for item in sorted(theirs - ours):
                print(f"  only expected:  {item}")  # noqa: T201
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
