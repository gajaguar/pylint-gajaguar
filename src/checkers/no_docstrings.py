from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from astroid.nodes import ClassDef
    from astroid.nodes import FunctionDef


class NoDocstringsChecker(BaseChecker):
    name = "app-no-docstrings"
    msgs = {  # noqa: RUF012
        "W9001": (
            "Docstring found in '%s'; use comments instead",
            "app-no-docstrings",
            "Functions, methods, and classes MUST NOT have docstrings.",
        )
    }

    def _check_docstring(self, node: FunctionDef | ClassDef) -> None:
        if node.doc_node is not None:
            self.add_message("app-no-docstrings", node=node.doc_node, args=(node.name,))

    def visit_functiondef(self, node: FunctionDef) -> None:
        self._check_docstring(node)

    def visit_classdef(self, node: ClassDef) -> None:
        self._check_docstring(node)

    visit_asyncfunctiondef = visit_functiondef
