from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from typing import Final

    from astroid.nodes import NodeNG
    from pylint.lint import PyLinter

DEFAULT_SECTION_MARKERS: Final[tuple[str, ...]] = ("Arrange", "Act", "Assert")

SECTION_MARKERS_OPTION: Final[Any] = (
    (
        "test-section-markers",
        {
            "default": DEFAULT_SECTION_MARKERS,
            "type": "csv",
            "metavar": "<names>",
            "help": (
                "Section names a test body must carry, in order, without the leading '# '. "
                "Every checker that reads test sections uses this one list."
            ),
        },
    ),
)

_TEST_DIRECTORY_NAMES: Final[frozenset[str]] = frozenset({"test", "tests"})


def section_markers(linter: PyLinter) -> tuple[str, ...]:
    environment_value = os.environ.get("TEST_SECTION_MARKERS", "")
    overridden = environment_value.split(" ") if environment_value else []
    configured = getattr(linter.config, "test_section_markers", None)
    names = overridden or configured or DEFAULT_SECTION_MARKERS
    return tuple(f"# {str(name).strip()}" for name in names)


def is_test_file(node: NodeNG) -> bool:
    filepath = node.root().file
    if not filepath:
        return False
    path = pathlib.Path(filepath)
    if path.stem.startswith("test_") or path.stem.endswith("_test"):
        return True
    return any(parent.name in _TEST_DIRECTORY_NAMES for parent in path.parents)


def is_test_function(node: NodeNG) -> bool:
    return bool(getattr(node, "name", "").startswith("test_")) and is_test_file(node)
