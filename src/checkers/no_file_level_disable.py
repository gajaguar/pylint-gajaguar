from __future__ import annotations

import re
import tokenize
from typing import TYPE_CHECKING
from typing import Final

from pylint.checkers import BaseTokenChecker

if TYPE_CHECKING:
    from collections.abc import Iterable
    from re import Pattern

_DISABLE_RE: Final[Pattern[str]] = re.compile(r"#\s*pylint:\s*disable=")
_DISABLE_NEXT_RE: Final[Pattern[str]] = re.compile(r"#\s*pylint:\s*disable-next=")

_NON_CODE: Final = frozenset({
    tokenize.NL,
    tokenize.NEWLINE,
    tokenize.COMMENT,
    tokenize.ENCODING,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.ENDMARKER,
})


class NoFileLevelDisableChecker(BaseTokenChecker):
    name = "app-no-file-level-disable"
    msgs = {  # noqa: RUF012
        "W9006": (
            "Standalone '# pylint: disable=' found; use inline or 'disable-next=' instead",
            "app-no-file-level-disable",
            "Lint suppressions must be inline or use disable-next, not standalone disables.",
        )
    }

    def process_tokens(self, tokens: Iterable[tokenize.TokenInfo]) -> None:
        lines_with_code = set()
        comments = []
        for tok_type, tok_string, (start_row, _), _, _ in tokens:
            if tok_type not in _NON_CODE:
                lines_with_code.add(start_row)
            if tok_type == tokenize.COMMENT:
                comments.append((start_row, tok_string))

        for lineno, text in comments:
            if _DISABLE_RE.search(text) and not _DISABLE_NEXT_RE.search(text) and lineno not in lines_with_code:
                self.add_message("app-no-file-level-disable", line=lineno)
