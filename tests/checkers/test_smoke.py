from __future__ import annotations

from pylint.testutils import CheckerTestCase

from checkers.smoke import SmokeChecker


class TestSmokeChecker(CheckerTestCase):
    CHECKER_CLASS = SmokeChecker

    def test_registers_with_no_messages(self) -> None:
        # Arrange
        checker = self.checker
        # Act
        message_count = len(checker.msgs)
        # Assert
        assert message_count == 0
