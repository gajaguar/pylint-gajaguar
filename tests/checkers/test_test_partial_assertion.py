from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.test_partial_assertion import TestPartialAssertionChecker as CheckerUnderTest
from tests.conftest import build_module_from_source
from tests.conftest import build_test_module_from_source
from tests.conftest import node_position

if TYPE_CHECKING:
    import pathlib


class TestTestPartialAssertionChecker(CheckerTestCase):
    CHECKER_CLASS = CheckerUnderTest

    def test_field_assertion_without_a_whole_object_assertion_fires(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = 'def test_thing():\n    assert response["count"] == 3\n'
        module = build_test_module_from_source(tmp_path, source)
        func = module.body[0]
        expected = MessageTest(
            "app-test-partial-assertion",
            node=func,
            args=("test_thing", "response"),
            **node_position(func),
        )
        # Act
        self.checker.visit_functiondef(func)
        # Assert
        assert self.linter.release_messages() == [expected]

    def test_whole_object_assertion_suppresses_the_message(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = 'def test_thing():\n    assert response["count"] == 3\n    assert response == {"count": 3}\n'
        module = build_test_module_from_source(tmp_path, source)
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_plain_assertion_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    assert value == 3\n"
        module = build_test_module_from_source(tmp_path, source)
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_subscript_outside_a_test_file_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = 'def test_thing():\n    assert response["count"] == 3\n'
        module = build_module_from_source(tmp_path, source)
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []
