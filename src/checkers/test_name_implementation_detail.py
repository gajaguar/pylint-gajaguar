from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Final

from pylint.checkers import BaseChecker

from checkers.scopes import is_test_function

if TYPE_CHECKING:
    from astroid.nodes import FunctionDef

_IMPLEMENTATION_TERMS: Final[tuple[str, ...]] = (
    "called",
    "calls",
    "impl",
    "internal",
    "mock",
    "patch",
    "private",
    "return_value",
    "spy",
    "stub",
)

_WORD_PATTERN: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+")


class TestNameImplementationDetailChecker(BaseChecker):
    name = "app-test-name-implementation-detail"
    msgs = {  # noqa: RUF012
        "W9017": (
            "Test name '%s' names an implementation detail: %s",
            "app-test-name-implementation-detail",
            "Test names SHOULD describe observable behavior, not how it is implemented.",
        )
    }

    def visit_functiondef(self, node: FunctionDef) -> None:
        if not is_test_function(node):
            return
        lowered = node.name.lower()
        words = set(_WORD_PATTERN.findall(lowered))
        # Single-word terms must match a whole word: 'implementation' is not 'impl'.
        found = [term for term in _IMPLEMENTATION_TERMS if (term in lowered if "_" in term else term in words)]
        if found:
            self.add_message(
                "app-test-name-implementation-detail",
                node=node,
                args=(node.name, ", ".join(sorted(set(found)))),
            )

    visit_asyncfunctiondef = visit_functiondef
