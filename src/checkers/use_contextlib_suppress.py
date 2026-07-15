from __future__ import annotations

from typing import TYPE_CHECKING

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import Try


class UseContextlibSuppressChecker(BaseChecker):
    name = "app-use-contextlib-suppress"
    msgs = {  # noqa: RUF012
        "W9012": (
            "Use 'contextlib.suppress(...)' instead of 'try/except/pass'",
            "app-use-contextlib-suppress",
            "When ignoring an expected exception, contextlib.suppress conveys intent explicitly.",
        )
    }

    def visit_try(self, node: Try) -> None:
        if not node.handlers:
            return
        if node.orelse or node.finalbody:
            return
        for handler in node.handlers:
            if handler.type is None:
                return
            body = handler.body
            if not (len(body) == 1 and isinstance(body[0], astroid.nodes.Pass)):
                return
        self.add_message("app-use-contextlib-suppress", node=node)
