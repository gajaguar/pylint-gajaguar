from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.test_aaa_markers import TestAAAMarkersChecker as AAAMarkersCheckerUnderTest
from tests.conftest import build_module_from_source
from tests.conftest import node_position

if TYPE_CHECKING:
    import pathlib


class TestTestAAAMarkersChecker(CheckerTestCase):
    CHECKER_CLASS = AAAMarkersCheckerUnderTest

    def test_missing_all_markers_fires(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_module_from_source(tmp_path, "def test_thing():\n    x = 1\n    assert x\n")
        func = module.body[0]
        self.checker.open()
        expected = MessageTest(
            "app-test-aaa-markers",
            node=func,
            args=("test_thing", "# Arrange, # Act, # Assert"),
            **node_position(func),
        )
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_missing_some_markers_fires_with_partial_list(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    # Arrange\n    x = 1\n    assert x\n"
        module = build_module_from_source(tmp_path, source)
        func = module.body[0]
        self.checker.open()
        expected = MessageTest(
            "app-test-aaa-markers",
            node=func,
            args=("test_thing", "# Act, # Assert"),
            **node_position(func),
        )
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == [expected]

    def test_all_markers_present_is_silent(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    # Arrange\n    x = 1\n    # Act\n    y = x\n    # Assert\n    assert y\n"
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
        module = build_module_from_source(tmp_path, "def helper():\n    return 1\n")
        func = module.body[0]
        self.checker.open()
        # Act
        self.checker.visit_functiondef(func)
        messages = self.linter.release_messages()
        # Assert
        assert messages == []
