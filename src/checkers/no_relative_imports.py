from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import ImportFrom


class NoRelativeImportsChecker(BaseChecker):
    name = "app-no-relative-imports"
    msgs = {  # noqa: RUF012
        "W9009": (
            "Relative import '%s' is not allowed; use absolute imports",
            "app-no-relative-imports",
            "Relative imports are forbidden in this project.",
        )
    }

    def visit_importfrom(self, node: ImportFrom) -> None:
        if node.level and node.level > 0:
            dots = "." * node.level
            modname = node.modname or ""
            self.add_message("app-no-relative-imports", node=node, args=(f"{dots}{modname}",))
