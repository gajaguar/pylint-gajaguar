from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.no_relative_imports import NoRelativeImportsChecker


class TestNoRelativeImportsChecker(CheckerTestCase):
    CHECKER_CLASS = NoRelativeImportsChecker

    def test_single_dot_relative_import_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("from . import foo")
        expected = MessageTest(
            "app-no-relative-imports",
            node=node,
            args=(".",),
            line=node.fromlineno,
            col_offset=node.col_offset,
            end_line=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        # Act
        self.checker.visit_importfrom(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_double_dot_relative_import_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("from ..pkg import foo")
        expected = MessageTest(
            "app-no-relative-imports",
            node=node,
            args=("..pkg",),
            line=node.fromlineno,
            col_offset=node.col_offset,
            end_line=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        # Act
        self.checker.visit_importfrom(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_absolute_import_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("from os import path")
        # Act
        self.checker.visit_importfrom(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
