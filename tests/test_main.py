from __future__ import annotations

from typing import Final

from pylint.lint import PyLinter

from main import register

EXPECTED_CHECKER_NAMES: Final = frozenset({
    "app-smoke",
    "app-no-docstrings",
    "app-test-aaa-markers",
    "app-test-no-blank-lines",
    "app-unused-arg-use-del",
    "app-no-relative-imports",
    "app-use-contextlib-suppress",
    "app-module-const-naming",
    "app-no-file-level-disable",
    "app-no-inline-imports",
    "app-frozenset-constant",
    "app-require-final",
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
