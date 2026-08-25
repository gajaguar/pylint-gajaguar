from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.test_name_implementation_detail import TestNameImplementationDetailChecker as CheckerUnderTest
from tests.conftest import build_module_from_source
from tests.conftest import build_test_module_from_source
from tests.conftest import node_position

if TYPE_CHECKING:
    import pathlib


class TestTestNameImplementationDetailChecker(CheckerTestCase):
    CHECKER_CLASS = CheckerUnderTest

    def test_name_naming_a_test_double_fires(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_test_module_from_source(tmp_path, "def test_mock_client_is_called():\n    assert True\n")
        func = module.body[0]
        expected = MessageTest(
            "app-test-name-implementation-detail",
            node=func,
            args=("test_mock_client_is_called", "called, mock"),
            **node_position(func),
        )
        # Act
        self.checker.visit_functiondef(func)
        # Assert
        assert self.linter.release_messages() == [expected]

    def test_a_word_merely_containing_a_term_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_test_module_from_source(tmp_path, "def test_implementation_is_hidden():\n    assert True\n")
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_behavioral_name_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_test_module_from_source(tmp_path, "def test_should_return_404():\n    assert True\n")
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_name_outside_a_test_file_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_module_from_source(tmp_path, "def test_mock_client():\n    assert True\n")
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []
