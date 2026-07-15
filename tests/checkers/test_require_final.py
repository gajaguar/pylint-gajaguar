from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.require_final import RequireFinalChecker


class TestRequireFinalChecker(CheckerTestCase):
    CHECKER_CLASS = RequireFinalChecker

    def test_bare_assignment_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("FOO = 1")
        expected = MessageTest(
            "app-require-final",
            node=node,
            args=("FOO",),
            line=node.fromlineno,
            col_offset=node.col_offset,
            end_line=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_non_final_annotation_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("FOO: int = 1")
        expected = MessageTest(
            "app-require-final",
            node=node,
            args=("FOO",),
            line=node.fromlineno,
            col_offset=node.col_offset,
            end_line=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        # Act
        self.checker.visit_annassign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_bare_final_annotation_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        from typing import Final
        FOO: Final = 1  #@
        """)
        # Act
        self.checker.visit_annassign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_subscripted_final_annotation_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        from typing import Final
        FOO: Final[int] = 1  #@
        """)
        # Act
        self.checker.visit_annassign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_typing_final_attribute_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        import typing
        FOO: typing.Final = 1  #@
        """)
        # Act
        self.checker.visit_annassign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_dunder_name_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("__all__ = []")
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_underscore_name_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("_ = 1")
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_tuple_unpacking_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("A, B = 1, 2")
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_non_module_scope_is_ignored(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo():
            bar = 1
            return bar
        """)
        assign = node.body[0]
        # Act
        self.checker.visit_assign(assign)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
