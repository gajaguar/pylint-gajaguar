from __future__ import annotations

import contextlib
import io
import pathlib
import tokenize
from typing import TYPE_CHECKING
from typing import Final

from pylint.checkers import BaseChecker

from checkers.scopes import is_test_function
from checkers.scopes import section_markers

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef
    from astroid.nodes import NodeNG
    from pylint.lint import PyLinter

# Pragmas change how tools behave; they are not explanatory prose.
_PRAGMA_PREFIXES: Final[tuple[str, ...]] = ("# noqa", "# pylint:", "# type:", "# mypy:", "# fmt:", "# ruff:")


class TestNoExtraCommentsChecker(BaseChecker):
    name = "app-test-no-extra-comments"
    msgs = {  # noqa: RUF012
        "W9015": (
            "Test method '%s' has an explanatory comment at line %d: %s",
            "app-test-no-extra-comments",
            "Test bodies MUST carry only the configured section markers.",
        )
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self._comments: dict[int, str] = {}
        self._loaded_filepath: str | None = None

    def open(self) -> None:
        self._comments = {}
        self._loaded_filepath = None

    def _load_comments(self, node: NodeNG) -> None:
        filepath = node.root().file
        if self._loaded_filepath == filepath:
            return
        self._comments = {}
        self._loaded_filepath = filepath
        if not filepath:
            return
        path = pathlib.Path(filepath)
        with contextlib.suppress(OSError, UnicodeDecodeError, tokenize.TokenError, SyntaxError):
            source = path.read_text(encoding="utf-8")
            for token in tokenize.generate_tokens(io.StringIO(source).readline):
                if token.type == tokenize.COMMENT:
                    self._comments[token.start[0]] = token.string.strip()

    def visit_functiondef(self, node: FunctionDef) -> None:
        if not is_test_function(node):
            return
        self._load_comments(node)
        if not self._comments:
            return
        allowed = set(section_markers(self.linter))
        for line in range(node.fromlineno, node.tolineno + 1):
            comment = self._comments.get(line)
            if comment is None or comment in allowed:
                continue
            if comment.startswith(_PRAGMA_PREFIXES):
                continue
            self.add_message(
                "app-test-no-extra-comments",
                line=line,
                node=node,
                args=(node.name, line, comment),
            )

    visit_asyncfunctiondef = visit_functiondef
