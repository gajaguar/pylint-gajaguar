from __future__ import annotations

import io
import tokenize

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.no_file_level_disable import NoFileLevelDisableChecker


def _tokens(source: str) -> list[tokenize.TokenInfo]:
    return list(tokenize.generate_tokens(io.StringIO(source).readline))


class TestNoFileLevelDisableChecker(CheckerTestCase):
    CHECKER_CLASS = NoFileLevelDisableChecker

    def test_standalone_disable_fires(self) -> None:
        # Arrange
        tokens = _tokens("x = 1\n# pylint: disable=invalid-name\ny = 2\n")
        expected = MessageTest("app-no-file-level-disable", line=2)
        # Act
        self.checker.process_tokens(tokens)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_inline_disable_is_silent(self) -> None:
        # Arrange
        tokens = _tokens("x = 1  # pylint: disable=invalid-name\n")
        # Act
        self.checker.process_tokens(tokens)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_disable_next_is_silent(self) -> None:
        # Arrange
        tokens = _tokens("# pylint: disable-next=invalid-name\nx = 1\n")
        # Act
        self.checker.process_tokens(tokens)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
