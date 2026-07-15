from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.use_contextlib_suppress import UseContextlibSuppressChecker


class TestUseContextlibSuppressChecker(CheckerTestCase):
    CHECKER_CLASS = UseContextlibSuppressChecker

    def test_try_except_pass_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        except ValueError:
            pass
        """)
        expected = MessageTest(
            "app-use-contextlib-suppress",
            node=node,
            line=node.fromlineno,
            col_offset=node.col_offset,
            end_line=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_bare_except_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        except:
            pass
        """)
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_except_with_else_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        except ValueError:
            pass
        else:
            do_other()
        """)
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_except_with_finally_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        except ValueError:
            pass
        finally:
            cleanup()
        """)
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_except_with_non_pass_body_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        except ValueError:
            log_error()
        """)
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_try_without_handlers_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        try:
            do_something()
        finally:
            cleanup()
        """)
        # Act
        self.checker.visit_try(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
