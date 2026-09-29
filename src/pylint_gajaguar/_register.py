from __future__ import annotations

from typing import TYPE_CHECKING

from pylint_gajaguar.frozenset_constant import FrozensetConstantChecker
from pylint_gajaguar.module_const_naming import ModuleConstNamingChecker
from pylint_gajaguar.no_docstrings import NoDocstringsChecker
from pylint_gajaguar.no_file_level_disable import NoFileLevelDisableChecker
from pylint_gajaguar.no_inline_imports import NoInlineImportsChecker
from pylint_gajaguar.no_relative_imports import NoRelativeImportsChecker
from pylint_gajaguar.require_final import RequireFinalChecker
from pylint_gajaguar.smoke import SmokeChecker
from pylint_gajaguar.test_aaa_markers import TestAAAMarkersChecker
from pylint_gajaguar.test_name_implementation_detail import TestNameImplementationDetailChecker
from pylint_gajaguar.test_no_blank_lines import TestNoBlankLinesChecker
from pylint_gajaguar.test_no_extra_comments import TestNoExtraCommentsChecker
from pylint_gajaguar.test_partial_assertion import TestPartialAssertionChecker
from pylint_gajaguar.unused_arg_use_del import UnusedArgUseDelChecker
from pylint_gajaguar.use_contextlib_suppress import UseContextlibSuppressChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: PyLinter) -> None:
    linter.register_checker(SmokeChecker(linter))
    linter.register_checker(NoDocstringsChecker(linter))
    linter.register_checker(TestAAAMarkersChecker(linter))
    linter.register_checker(TestNoBlankLinesChecker(linter))
    linter.register_checker(TestNoExtraCommentsChecker(linter))
    linter.register_checker(TestPartialAssertionChecker(linter))
    linter.register_checker(TestNameImplementationDetailChecker(linter))
    linter.register_checker(UnusedArgUseDelChecker(linter))
    linter.register_checker(NoRelativeImportsChecker(linter))
    linter.register_checker(UseContextlibSuppressChecker(linter))
    linter.register_checker(ModuleConstNamingChecker(linter))
    linter.register_checker(NoFileLevelDisableChecker(linter))
    linter.register_checker(NoInlineImportsChecker(linter))
    linter.register_checker(FrozensetConstantChecker(linter))
    linter.register_checker(RequireFinalChecker(linter))
