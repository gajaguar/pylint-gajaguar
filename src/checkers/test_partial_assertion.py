from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes
from pylint.checkers import BaseChecker

from checkers.scopes import is_test_function

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef


def _subscript_root(node: nodes.NodeNG) -> str | None:
    current = node
    while isinstance(current, nodes.Subscript):
        current = current.value
    if isinstance(current, nodes.Name) and current is not node:
        return str(current.name)
    return None


def _compared_names(test: nodes.NodeNG) -> tuple[set[str], set[str]]:
    subscripted: set[str] = set()
    whole: set[str] = set()
    if not isinstance(test, nodes.Compare):
        return subscripted, whole
    operands = [test.left, *(operand for _, operand in test.ops)]
    for operand in operands:
        root = _subscript_root(operand)
        if root is not None:
            subscripted.add(root)
        elif isinstance(operand, nodes.Name):
            whole.add(operand.name)
    return subscripted, whole


class TestPartialAssertionChecker(BaseChecker):
    name = "app-test-partial-assertion"
    msgs = {  # ruff: ignore[mutable-class-default]
        "W9016": (
            "Test method '%s' asserts on '%s[...]' without ever asserting the whole object",
            "app-test-partial-assertion",
            "Tests SHOULD assert whole objects rather than individual fields.",
        )
    }

    def visit_functiondef(self, node: FunctionDef) -> None:
        if not is_test_function(node):
            return
        subscripted: set[str] = set()
        whole: set[str] = set()
        for assertion in node.nodes_of_class(nodes.Assert):
            partial_names, whole_names = _compared_names(assertion.test)
            subscripted |= partial_names
            whole |= whole_names
        for name in sorted(subscripted - whole):
            self.add_message("app-test-partial-assertion", node=node, args=(node.name, name))

    visit_asyncfunctiondef = visit_functiondef
