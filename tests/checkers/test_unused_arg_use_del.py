from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.unused_arg_use_del import UnusedArgUseDelChecker


class TestUnusedArgUseDelChecker(CheckerTestCase):
    CHECKER_CLASS = UnusedArgUseDelChecker

    def test_unused_underscore_arg_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo(_bar):
            return 1
        """)
        arg = node.args.args[0]
        expected = MessageTest(
            "app-unused-arg-use-del",
            node=arg,
            args=("_bar", "_bar"),
            line=arg.fromlineno,
            col_offset=arg.col_offset,
            end_line=arg.end_lineno,
            end_col_offset=arg.end_col_offset,
        )
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_used_underscore_arg_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo(_bar):
            return _bar
        """)
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_self_and_cls_are_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        class Foo:
            def bar(self, cls):
                return 1
        """).body[0]
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_single_underscore_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo(_):
            return 1
        """)
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_dunder_prefixed_is_skipped(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo(__bar):
            return 1
        """)
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_plain_unused_arg_is_not_flagged(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def foo(bar):
            return 1
        """)
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
