from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Final

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from re import Pattern

    from astroid.nodes import AssignName

_SCREAMING: Final[Pattern[str]] = re.compile(r"^_?[A-Z][A-Z0-9_]*$")
_DUNDER: Final[Pattern[str]] = re.compile(r"^__\w+__$")


class ModuleConstNamingChecker(BaseChecker):
    name = "app-module-const-naming"
    msgs = {  # noqa: RUF012
        "C9005": (
            "Module-level name '%s' should be SCREAMING_SNAKE_CASE",
            "app-module-const-naming",
            "Module-level variables are treated as constants and must use SCREAMING_SNAKE_CASE.",
        )
    }

    def visit_assignname(self, node: AssignName) -> None:
        if not isinstance(node.frame(), astroid.nodes.Module):
            return
        name = node.name
        if _DUNDER.match(name) or name == "_":
            return
        if not _SCREAMING.match(name):
            self.add_message("app-module-const-naming", node=node, args=(name,))
