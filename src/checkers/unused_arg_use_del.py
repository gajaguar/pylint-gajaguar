from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

import astroid.nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef

_SKIP_NAMES: Final[frozenset[str]] = frozenset({"self", "cls"})


def _collect_name_usages(func_node: astroid.nodes.FunctionDef) -> frozenset[str]:
    return frozenset(child.name for child in func_node.nodes_of_class(astroid.nodes.Name))


class UnusedArgUseDelChecker(BaseChecker):
    name = "app-unused-arg-use-del"
    msgs = {  # noqa: RUF012
        "W9004": (
            "Argument '%s' uses leading underscore; use 'del %s' at the top of the body instead",
            "app-unused-arg-use-del",
            "Unused function arguments MUST be discarded via `del arg`, not renamed with a leading underscore.",
        )
    }

    def visit_functiondef(self, node: FunctionDef) -> None:
        all_args = list(node.args.args or []) + list(node.args.kwonlyargs or []) + list(node.args.posonlyargs or [])
        used_names = _collect_name_usages(node)
        for arg in all_args:
            arg_name = arg.name
            if arg_name in _SKIP_NAMES:
                continue
            if not (arg_name.startswith("_") and arg_name != "_" and not arg_name.startswith("__")):
                continue
            if arg_name in used_names:
                continue
            self.add_message("app-unused-arg-use-del", node=arg, args=(arg_name, arg_name))

    visit_asyncfunctiondef = visit_functiondef
