from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from checkers.test_no_extra_comments import TestNoExtraCommentsChecker as CheckerUnderTest
from tests.conftest import build_module_from_source
from tests.conftest import build_test_module_from_source
from tests.conftest import node_position

if TYPE_CHECKING:
    import pathlib

MARKED_BODY: Final = "def test_thing():\n    # Arrange\n    x = 1\n    # Act\n    y = x\n    # Assert\n    assert y\n"


class TestTestNoExtraCommentsChecker(CheckerTestCase):
    CHECKER_CLASS = CheckerUnderTest

    def test_section_markers_alone_do_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_test_module_from_source(tmp_path, MARKED_BODY)
        self.checker.open()
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_explanatory_comment_fires(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    # Arrange\n    # builds the widget\n    x = 1\n"
        module = build_test_module_from_source(tmp_path, source)
        func = module.body[0]
        self.checker.open()
        position = {**node_position(func), "line": 3}
        expected = MessageTest(
            "app-test-no-extra-comments",
            node=func,
            args=("test_thing", 3, "# builds the widget"),
            **position,
        )
        # Act
        self.checker.visit_functiondef(func)
        # Assert
        assert self.linter.release_messages() == [expected]

    def test_pragma_comment_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    # Arrange\n    x = 1  # noqa: E501\n"
        module = build_test_module_from_source(tmp_path, source)
        self.checker.open()
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []

    def test_comment_outside_a_test_file_does_not_fire(self, tmp_path: pathlib.Path) -> None:
        # Arrange
        source = "def test_thing():\n    # explanatory\n    x = 1\n"
        module = build_module_from_source(tmp_path, source)
        self.checker.open()
        # Act
        self.checker.visit_functiondef(module.body[0])
        # Assert
        assert self.linter.release_messages() == []
