from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from checkers.scopes import DEFAULT_SECTION_MARKERS
from checkers.scopes import is_test_file
from checkers.scopes import is_test_function
from checkers.scopes import section_markers
from tests.conftest import build_module_from_source
from tests.conftest import build_test_module_from_source

if TYPE_CHECKING:
    import pathlib

    import pytest


@dataclass(frozen=True)
class FakeConfig:
    test_section_markers: list[str] | None


@dataclass(frozen=True)
class FakeLinter:
    config: FakeConfig


class TestTestScope:
    @staticmethod
    def test_a_test_named_module_is_a_test_file(tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_test_module_from_source(tmp_path, "x = 1\n")
        # Act
        result = is_test_file(module)
        # Assert
        assert result is True

    @staticmethod
    def test_a_plain_module_is_not_a_test_file(tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_module_from_source(tmp_path, "x = 1\n")
        # Act
        result = is_test_file(module)
        # Assert
        assert result is False

    @staticmethod
    def test_a_test_prefixed_symbol_outside_a_test_file_is_not_a_test_function(tmp_path: pathlib.Path) -> None:
        # Arrange
        module = build_module_from_source(tmp_path, "def test_report():\n    return 1\n")
        # Act
        result = is_test_function(module.body[0])
        # Assert
        assert result is False

    @staticmethod
    def test_section_markers_fall_back_to_the_default(tmp_path: pathlib.Path) -> None:
        # Arrange
        linter = FakeLinter(FakeConfig(None))
        # Act
        markers = section_markers(linter)
        # Assert
        assert markers == tuple(f"# {name}" for name in DEFAULT_SECTION_MARKERS)

    @staticmethod
    def test_section_markers_read_the_configured_list(tmp_path: pathlib.Path) -> None:
        # Arrange
        linter = FakeLinter(FakeConfig([" Setup", "Action ", "Expected"]))
        # Act
        markers = section_markers(linter)
        # Assert
        assert markers == ("# Setup", "# Action", "# Expected")

    @staticmethod
    def test_section_markers_are_overridden_by_the_environment_variable(monkeypatch: pytest.MonkeyPatch) -> None:
        # Arrange
        monkeypatch.setenv("TEST_SECTION_MARKERS", "Given When Then")
        linter = FakeLinter(FakeConfig(["Setup", "Action", "Expected"]))
        # Act
        markers = section_markers(linter)
        # Assert
        assert markers == ("# Given", "# When", "# Then")

    @staticmethod
    def test_section_markers_fall_back_to_the_configured_list_when_the_environment_variable_is_unset(
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # Arrange
        monkeypatch.delenv("TEST_SECTION_MARKERS", raising=False)
        linter = FakeLinter(FakeConfig(["Given", "When", "Then"]))
        # Act
        markers = section_markers(linter)
        # Assert
        assert markers == ("# Given", "# When", "# Then")
