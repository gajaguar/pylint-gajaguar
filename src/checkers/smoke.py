from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.typing import ExtraMessageOptions


class SmokeChecker(BaseChecker):
    name = "app-smoke"
    msgs: dict[str, tuple[str, str, str] | tuple[str, str, str, ExtraMessageOptions]] = {}  # noqa: RUF012
