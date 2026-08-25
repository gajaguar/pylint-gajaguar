from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING
from typing import Any
from typing import Final

if TYPE_CHECKING:
    from astroid.nodes import NodeNG
    from pylint.lint import PyLinter

DEFAULT_SECTION_MARKERS: Final[tuple[str, ...]] = ("# Arrange", "# Act", "# Assert")

SECTION_MARKERS_OPTION: Final[Any] = (
    (
        "test-section-markers",
        {
            "default": DEFAULT_SECTION_MARKERS,
            "type": "csv",
            "metavar": "<markers>",
            "help": (
                "Section comments a test body must carry, in order. "
                "Every checker that reads test sections uses this one list."
            ),
        },
    ),
)

_TEST_DIRECTORY_NAMES: Final[frozenset[str]] = frozenset({"test", "tests"})


def section_markers(linter: PyLinter) -> tuple[str, ...]:
    configured = getattr(linter.config, "test_section_markers", None)
    if not configured:
        return DEFAULT_SECTION_MARKERS
    return tuple(str(marker).strip() for marker in configured)


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
