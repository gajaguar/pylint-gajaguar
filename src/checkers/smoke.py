from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.typing import ExtraMessageOptions

    type _MSGS_VAL = tuple[str, str, str] | tuple[str, str, str, ExtraMessageOptions]  # pylint: disable=invalid-name


class SmokeChecker(BaseChecker):
    name = "app-smoke"
    msgs: dict[str, _MSGS_VAL] = {}  # ruff: ignore[mutable-class-default]
