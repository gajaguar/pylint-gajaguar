from __future__ import annotations

from typing import TYPE_CHECKING

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import AnnAssign
    from astroid.nodes import Assign
    from astroid.nodes import NodeNG


def _is_mutable_set(value: NodeNG) -> bool:
    if isinstance(value, astroid.nodes.Set | astroid.nodes.SetComp):
        return True
    if isinstance(value, astroid.nodes.Call):
        func = value.func
        if isinstance(func, astroid.nodes.Name):
            return bool(func.name == "set")
        if isinstance(func, astroid.nodes.Attribute):
            return bool(func.attrname == "set")
    return False


class FrozensetConstantChecker(BaseChecker):
    name = "app-frozenset-constant"
    msgs = {  # noqa: RUF012
        "W9013": (
            "Set constant should be a frozenset(...) for immutability",
            "app-frozenset-constant",
            "Module-level set constants are mutable; use frozenset(...) to prevent accidental mutation.",
        )
    }

    def visit_assign(self, node: Assign) -> None:
        if not isinstance(node.frame(), astroid.nodes.Module):
            return
        if _is_mutable_set(node.value):
            self.add_message("app-frozenset-constant", node=node.value)

    def visit_annassign(self, node: AnnAssign) -> None:
        if not isinstance(node.frame(), astroid.nodes.Module):
            return
        if node.value is not None and _is_mutable_set(node.value):
            self.add_message("app-frozenset-constant", node=node.value)
