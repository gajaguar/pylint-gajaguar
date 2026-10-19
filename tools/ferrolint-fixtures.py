#!/usr/bin/env python3
"""Compare the ferrolint plugin with the pylint plugin on the fixtures.

ferrolint/fixtures/<CODE>*/*.py are linted by both. For the rule <CODE> (GAJ0nn
is pylint message 9"0nn"), the (file, line, message) triples must be equal.
A directory may add a suffix (GAJ015-markers) and an options.json, a flat
object of option name to text: ferrolint reads it as the plugin's options,
pylint as --name=value.

Usage: ferrolint-fixtures.py WASM [CODE ...]
Environment: FERROLINT (the binary, default "ferrolint"), PYLINT (default
"uv run pylint").
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
FIXTURES = ROOT / "ferrolint" / "fixtures"


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


def pylint(command: str, code: str, directory: pathlib.Path, options: dict[str, str]) -> set[tuple[str, int, str]]:
    run = subprocess.run(
        [
            *shlex.split(command),
            "--load-plugins=pylint_gajaguar",
            "--disable=all",
            "--enable=gajaguar",
            *(f"--{name}={value}" for name, value in options.items()),
            "--msg-template={path}\t{line}\t{msg_id}\t{msg}",
            str(directory),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    result = set()
    for row in run.stdout.splitlines():
        parts = row.split("\t")
        if len(parts) == 4 and parts[2][1:] == "9" + code[3:]:  # noqa: PLR2004
            result.add(((ROOT / parts[0]).relative_to(directory).as_posix(), int(parts[1]), parts[3]))
    return result


def main() -> int:
    wasm = pathlib.Path(sys.argv[1]).resolve()
    wanted = set(sys.argv[2:])
    binary = os.environ.get("FERROLINT", "ferrolint")
    command = os.environ.get("PYLINT", "uv run pylint")
    failed = False
    for directory in sorted(FIXTURES.iterdir()):
        code = directory.name[:6]
        if wanted and code not in wanted:
            continue
        settings = directory / "options.json"
        options = json.loads(settings.read_text()) if settings.exists() else {}
        ours = ferrolint(binary, wasm, code, directory, options)
        theirs = pylint(command, code, directory, options)
        if not theirs:
            sys.exit(f"{directory.name}: pylint found nothing; the fixtures prove nothing")
        status = "ok" if ours == theirs else "DIFF"
        print(f"{directory.name}: {status} ({len(theirs)} findings)")  # noqa: T201
        if ours != theirs:
            failed = True
            for item in sorted(ours - theirs):
                print(f"  only ferrolint: {item}")  # noqa: T201
            for item in sorted(theirs - ours):
                print(f"  only pylint:    {item}")  # noqa: T201
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
