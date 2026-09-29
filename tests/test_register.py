from __future__ import annotations

from typing import Final

from pylint.lint import PyLinter

from pylint_gajaguar import register

EXPECTED_CHECKER_NAMES: Final = frozenset({
    "gajaguar-smoke",
    "gajaguar-no-docstrings",
    "gajaguar-test-aaa-markers",
    "gajaguar-test-no-blank-lines",
    "gajaguar-test-no-extra-comments",
    "gajaguar-test-partial-assertion",
    "gajaguar-test-name-implementation-detail",
    "gajaguar-unused-arg-use-del",
    "gajaguar-no-relative-imports",
    "gajaguar-use-contextlib-suppress",
    "gajaguar-module-const-naming",
    "gajaguar-no-file-level-disable",
    "gajaguar-no-inline-imports",
    "gajaguar-frozenset-constant",
    "gajaguar-require-final",
})


class TestRegister:
    @staticmethod
    def test_registers_every_checker_exactly_once() -> None:
        # Arrange
        linter = PyLinter()
        before = {id(checker) for checkers in linter._checkers.values() for checker in checkers}
        # Act
        register(linter)
        # Assert
        after = {
            checker for checkers in linter._checkers.values() for checker in checkers if id(checker) not in before
        }
        names = {checker.name for checker in after}
        assert names == EXPECTED_CHECKER_NAMES
        assert len(after) == len(EXPECTED_CHECKER_NAMES)
