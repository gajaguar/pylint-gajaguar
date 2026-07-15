from __future__ import annotations

import contextlib
import pathlib
from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef
    from astroid.nodes import NodeNG
    from pylint.lint import PyLinter


class TestNoBlankLinesChecker(BaseChecker):
    name = "app-test-no-blank-lines"
    msgs = {  # noqa: RUF012
        "W9003": (
            "Test method '%s' contains a blank line at line %d",
            "app-test-no-blank-lines",
            "Test method bodies MUST NOT contain blank lines.",
        )
    }

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
        if not node.name.startswith("test_"):
            return
        self._load_lines(node)
        if not self._lines:
            return
        # fromlineno is the def line (1-indexed); body starts at next line
        start = node.fromlineno  # 0-indexed index of first body line
        end = node.tolineno
        for index in range(start, end):
            if index < len(self._lines) and not self._lines[index].strip():
                self.add_message(
                    "app-test-no-blank-lines",
                    line=index + 1,
                    node=node,
                    args=(node.name, index + 1),
                )
                break

    visit_asyncfunctiondef = visit_functiondef
