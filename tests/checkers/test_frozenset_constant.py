from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.frozenset_constant import FrozensetConstantChecker


class TestFrozensetConstantChecker(CheckerTestCase):
    CHECKER_CLASS = FrozensetConstantChecker

    def test_set_literal_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("BAD = {1, 2, 3}")
        value = node.value
        expected = MessageTest(
            "app-frozenset-constant",
            node=value,
            line=value.fromlineno,
            col_offset=value.col_offset,
            end_line=value.end_lineno,
            end_col_offset=value.end_col_offset,
        )
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_set_comprehension_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("BAD = {x for x in range(3)}")
        value = node.value
        expected = MessageTest(
            "app-frozenset-constant",
            node=value,
            line=value.fromlineno,
            col_offset=value.col_offset,
            end_line=value.end_lineno,
            end_col_offset=value.end_col_offset,
        )
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_set_call_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("BAD = set([1, 2, 3])")
        value = node.value
        expected = MessageTest(
            "app-frozenset-constant",
            node=value,
            line=value.fromlineno,
            col_offset=value.col_offset,
            end_line=value.end_lineno,
            end_col_offset=value.end_col_offset,
        )
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_frozenset_call_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("GOOD = frozenset({1, 2, 3})")
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_annassign_set_literal_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("BAD: set[int] = {1, 2, 3}")
        value = node.value
        expected = MessageTest(
            "app-frozenset-constant",
            node=value,
            line=value.fromlineno,
            col_offset=value.col_offset,
            end_line=value.end_lineno,
            end_col_offset=value.end_col_offset,
        )
        # Act
        self.checker.visit_annassign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_dict_literal_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("GOOD = {'a': 1}")
        # Act
        self.checker.visit_assign(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_non_module_scope_is_ignored(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo():
            bad = {1, 2, 3}
            return bad
        """)
        assign = node.body[0]
        # Act
        self.checker.visit_assign(assign)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
