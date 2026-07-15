from __future__ import annotations

from typing import TYPE_CHECKING

from checkers.frozenset_constant import FrozensetConstantChecker
from checkers.module_const_naming import ModuleConstNamingChecker
from checkers.no_docstrings import NoDocstringsChecker
from checkers.no_file_level_disable import NoFileLevelDisableChecker
from checkers.no_inline_imports import NoInlineImportsChecker
from checkers.no_relative_imports import NoRelativeImportsChecker
from checkers.require_final import RequireFinalChecker
from checkers.smoke import SmokeChecker
from checkers.test_aaa_markers import TestAAAMarkersChecker
from checkers.test_no_blank_lines import TestNoBlankLinesChecker
from checkers.unused_arg_use_del import UnusedArgUseDelChecker
from checkers.use_contextlib_suppress import UseContextlibSuppressChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: PyLinter) -> None:
    linter.register_checker(SmokeChecker(linter))
    linter.register_checker(NoDocstringsChecker(linter))
    linter.register_checker(TestAAAMarkersChecker(linter))
    linter.register_checker(TestNoBlankLinesChecker(linter))
    linter.register_checker(UnusedArgUseDelChecker(linter))
    linter.register_checker(NoRelativeImportsChecker(linter))
    linter.register_checker(UseContextlibSuppressChecker(linter))
    linter.register_checker(ModuleConstNamingChecker(linter))
    linter.register_checker(NoFileLevelDisableChecker(linter))
    linter.register_checker(NoInlineImportsChecker(linter))
    linter.register_checker(FrozensetConstantChecker(linter))
    linter.register_checker(RequireFinalChecker(linter))
