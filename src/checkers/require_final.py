from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Final

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from re import Pattern

    from astroid.nodes import AnnAssign
    from astroid.nodes import Assign
    from astroid.nodes import NodeNG

_DUNDER: Final[Pattern[str]] = re.compile(r"^__\w+__$")


def _is_final(annotation: NodeNG) -> bool:
    if isinstance(annotation, astroid.nodes.Subscript):
        return _is_final(annotation.value)
    if isinstance(annotation, astroid.nodes.Name):
        return bool(annotation.name == "Final")
    if isinstance(annotation, astroid.nodes.Attribute):
        return bool(annotation.attrname == "Final")
    return False


def _skip_name(name: str) -> bool:
    return bool(_DUNDER.match(name) or name == "_")


class RequireFinalChecker(BaseChecker):
    name = "app-require-final"
    msgs = {  # noqa: RUF012
        "C9014": (
            "Module-level constant '%s' must be annotated Final",
            "app-require-final",
            "Module-level constants must carry a Final annotation to make immutability explicit.",
        )
    }

    def visit_assign(self, node: Assign) -> None:
        if not isinstance(node.frame(), astroid.nodes.Module):
            return
        if len(node.targets) != 1 or not isinstance(node.targets[0], astroid.nodes.AssignName):
            return
        name = node.targets[0].name
        if _skip_name(name):
            return
        self.add_message("app-require-final", node=node, args=(name,))

    def visit_annassign(self, node: AnnAssign) -> None:
        if not isinstance(node.frame(), astroid.nodes.Module):
            return
        if not isinstance(node.target, astroid.nodes.AssignName):
            return
        name = node.target.name
        if _skip_name(name):
            return
        if not _is_final(node.annotation):
            self.add_message("app-require-final", node=node, args=(name,))
