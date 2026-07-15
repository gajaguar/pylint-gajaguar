from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.test_no_blank_lines import TestNoBlankLinesChecker as NoBlankLinesCheckerUnderTest
from tests.conftest import build_module_from_source
from tests.conftest import node_position

if TYPE_CHECKING:
    import pathlib


class TestTestNoBlankLinesChecker(CheckerTestCase):
    CHECKER_CLASS = NoBlankLinesCheckerUnderTest

    def test_blank_line_in_body_fires(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    x = 1\n\n    assert x\n"
        module = build_module_from_source(tmp_path, source)
        func = module.body[0]
        self.checker.open()
        position = node_position(func)
        position["line"] = 3
        expected = MessageTest("app-test-no-blank-lines", node=func, args=("test_thing", 3), **position)
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_no_blank_line_is_silent(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    x = 1\n    assert x\n"
        module = build_module_from_source(tmp_path, source)
        func = module.body[0]
        self.checker.open()
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []

    def test_non_test_function_is_ignored(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def helper():\n    x = 1\n\n    return x\n"
        module = build_module_from_source(tmp_path, source)
        func = module.body[0]
        self.checker.open()
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
