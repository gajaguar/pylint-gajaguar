from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.no_inline_imports import NoInlineImportsChecker


class TestNoInlineImportsChecker(CheckerTestCase):
    CHECKER_CLASS = NoInlineImportsChecker

    def test_import_inside_function_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo():
            import os
            return os
        """)
        import_node = node.body[0]
        expected = MessageTest(
            "app-no-inline-imports",
            node=import_node,
            args=("os", "FunctionDef"),
            line=import_node.fromlineno,
            col_offset=import_node.col_offset,
            end_line=import_node.end_lineno,
            end_col_offset=import_node.end_col_offset,
        )
        # Act
        self.checker.visit_import(import_node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_import_at_module_top_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("import os")
        # Act
        self.checker.visit_import(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_importfrom_inside_function_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo():
            from os import path
            return path
        """)
        importfrom_node = node.body[0]
        expected = MessageTest(
            "app-no-inline-imports",
            node=importfrom_node,
            args=("path", "FunctionDef"),
            line=importfrom_node.fromlineno,
            col_offset=importfrom_node.col_offset,
            end_line=importfrom_node.end_lineno,
            end_col_offset=importfrom_node.end_col_offset,
        )
        # Act
        self.checker.visit_importfrom(importfrom_node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_importfrom_at_module_top_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("from os import path")
        # Act
        self.checker.visit_importfrom(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_importfrom_under_type_checking_guard_is_silent(self) -> None:
        # Arrange
        module = astroid.parse("""
        from typing import TYPE_CHECKING
        if TYPE_CHECKING:
            from os import path
        """)
        importfrom_node = module.body[1].body[0]
        # Act
        self.checker.visit_importfrom(importfrom_node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
