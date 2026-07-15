from __future__ import annotations

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.no_docstrings import NoDocstringsChecker


class TestNoDocstringsChecker(CheckerTestCase):
    CHECKER_CLASS = NoDocstringsChecker

    def test_function_with_docstring_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def greet():
            '''hello'''
            return 1
        """)
        doc_node = node.doc_node
        expected = MessageTest(
            "app-no-docstrings",
            node=doc_node,
            args=("greet",),
            line=doc_node.fromlineno,
            col_offset=doc_node.col_offset,
            end_line=doc_node.end_lineno,
            end_col_offset=doc_node.end_col_offset,
        )
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_function_without_docstring_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        def greet():
            return 1
        """)
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_method_with_docstring_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        class Foo:
            def bar(self):
                '''hi'''
                return 1
        """).body[0]
        doc_node = node.doc_node
        expected = MessageTest(
            "app-no-docstrings",
            node=doc_node,
            args=("bar",),
            line=doc_node.fromlineno,
            col_offset=doc_node.col_offset,
            end_line=doc_node.end_lineno,
            end_col_offset=doc_node.end_col_offset,
        )
        # Act
        self.checker.visit_functiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_class_with_docstring_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        class Foo:
            '''hi'''
        """)
        doc_node = node.doc_node
        expected = MessageTest(
            "app-no-docstrings",
            node=doc_node,
            args=("Foo",),
            line=doc_node.fromlineno,
            col_offset=doc_node.col_offset,
            end_line=doc_node.end_lineno,
            end_col_offset=doc_node.end_col_offset,
        )
        # Act
        self.checker.visit_classdef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_class_without_docstring_is_silent(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        class Foo:
            x = 1
        """)
        # Act
        self.checker.visit_classdef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_async_function_with_docstring_fires(self) -> None:
        # Arrange
        node = astroid.extract_node("""
        async def greet():
            '''hello'''
            return 1
        """)
        doc_node = node.doc_node
        expected = MessageTest(
            "app-no-docstrings",
            node=doc_node,
            args=("greet",),
            line=doc_node.fromlineno,
            col_offset=doc_node.col_offset,
            end_line=doc_node.end_lineno,
            end_col_offset=doc_node.end_col_offset,
        )
        # Act
        self.checker.visit_asyncfunctiondef(node)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]
