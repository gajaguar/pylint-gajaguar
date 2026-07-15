from __future__ import annotations

from typing import TYPE_CHECKING

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import Import
    from astroid.nodes import ImportFrom
    from astroid.nodes import NodeNG


class NoInlineImportsChecker(BaseChecker):
    name = "app-no-inline-imports"
    msgs = {  # noqa: RUF012
        "W9008": (
            "Import of '%s' inside %s; move to top of module",
            "app-no-inline-imports",
            "Inline imports are strictly forbidden; they usually indicate circular import issues.",
        )
    }

    def _check(self, node: Import | ImportFrom) -> None:
        if isinstance(node.frame(), astroid.nodes.Module):
            return
        frame = node.frame()
        frame_type = type(frame).__name__
        if hasattr(node, "names"):
            names = ", ".join(alias[1] or alias[0] for alias in node.names)
        else:
            names = node.modname or "?"
        self.add_message("app-no-inline-imports", node=node, args=(names, frame_type))

    def visit_import(self, node: Import) -> None:
        self._check(node)

    @staticmethod
    def _is_type_checking_guard(test_node: NodeNG) -> bool:
        if isinstance(test_node, astroid.nodes.Name):
            return bool(test_node.name == "TYPE_CHECKING")
        if isinstance(test_node, astroid.nodes.Attribute):
            return bool(test_node.attrname == "TYPE_CHECKING")
        return False

    def visit_importfrom(self, node: ImportFrom) -> None:
        parent = node.parent
        if isinstance(parent, astroid.nodes.If) and self._is_type_checking_guard(parent.test):
            return
        self._check(node)
