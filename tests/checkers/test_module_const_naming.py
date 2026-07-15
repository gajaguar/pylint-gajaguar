from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.module_const_naming import ModuleConstNamingChecker


class TestModuleConstNamingChecker(CheckerTestCase):
    CHECKER_CLASS = ModuleConstNamingChecker

    def test_lowercase_module_name_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("lower_name = 1")
        assign_name = node.targets[0]
        expected = MessageTest(
            "app-module-const-naming",
            node=assign_name,
            args=("lower_name",),
            line=assign_name.fromlineno,
            col_offset=assign_name.col_offset,
            end_line=assign_name.end_lineno,
            end_col_offset=assign_name.end_col_offset,
        )
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_screaming_snake_case_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("SCREAMING_NAME = 1")
        assign_name = node.targets[0]
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_private_screaming_snake_case_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("_PRIVATE_NAME = 1")
        assign_name = node.targets[0]
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_dunder_name_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("__all__ = []")
        assign_name = node.targets[0]
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_underscore_name_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("_ = 1")
        assign_name = node.targets[0]
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_non_module_scope_is_ignored(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo():
            lower_name = 1
            return lower_name
        """)
        assign_name = node.body[0].targets[0]
        # Act
        self.checker.visit_assignname(assign_name)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
