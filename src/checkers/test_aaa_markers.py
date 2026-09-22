from __future__ import annotations

import contextlib
import pathlib
from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

from checkers.scopes import SECTION_MARKERS_OPTION
from checkers.scopes import is_test_function
from checkers.scopes import section_markers

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef
    from astroid.nodes import NodeNG
    from pylint.lint import PyLinter


class TestAAAMarkersChecker(BaseChecker):
    name = "app-test-aaa-markers"
    msgs = {  # ruff: ignore[mutable-class-default]
        "W9002": (
            "Test method '%s' missing AAA marker(s): %s",
            "app-test-aaa-markers",
            "Test methods must carry every configured section marker.",
        )
    }

    options = SECTION_MARKERS_OPTION

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self._lines: list[str] = []
        self._loaded_filepath: str | None = None

    def open(self) -> None:
        self._lines = []
        self._loaded_filepath = None

    def _load_lines(self, node: NodeNG) -> None:
        filepath = node.root().file
        if self._lines and self._loaded_filepath == filepath:
            return
        self._lines = []
        if filepath:
            path = pathlib.Path(filepath)
            with contextlib.suppress(OSError, UnicodeDecodeError), path.open(encoding="utf-8") as file_handle:
                self._lines = file_handle.readlines()
            self._loaded_filepath = filepath

    def visit_functiondef(self, node: FunctionDef) -> None:
        if not is_test_function(node):
            return
        self._load_lines(node)
        if not self._lines:
            return
        start = node.fromlineno - 1
        end = node.tolineno
        raw = "".join(self._lines[start:end])
        missing = [marker for marker in section_markers(self.linter) if marker not in raw]
        if missing:
            self.add_message(
                "app-test-aaa-markers",
                node=node,
                args=(node.name, ", ".join(missing)),
            )

    visit_asyncfunctiondef = visit_functiondef
