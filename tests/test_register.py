from __future__ import annotations

from typing import Final

from pylint.lint import PyLinter

from pylint_gajaguar import register

CHECKER_NAME: Final = "gajaguar"
CHECKER_COUNT: Final = 15


class TestRegister:
    @staticmethod
    def test_registers_every_checker_exactly_once() -> None:
        # Arrange
        linter = PyLinter()
        before = {id(checker) for checkers in linter._checkers.values() for checker in checkers}
        # Act
        register(linter)
        # Assert
        after = [
            checker for checkers in linter._checkers.values() for checker in checkers if id(checker) not in before
        ]
        assert len(after) == CHECKER_COUNT
        assert {checker.name for checker in after} == {CHECKER_NAME}

    @staticmethod
    def test_enabling_the_checker_name_enables_every_message() -> None:
        # Arrange
        linter = PyLinter()
        register(linter)
        linter.disable("all")
        symbols = [
            message[1]
            for checker in linter.get_checkers()
            if checker.name == CHECKER_NAME
            for message in checker.msgs.values()
        ]
        # Act
        linter.enable(CHECKER_NAME)
        # Assert
        assert symbols
        assert all(linter.is_message_enabled(symbol) for symbol in symbols)
