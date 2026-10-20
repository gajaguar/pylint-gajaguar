import functools


@functools.cache
def decorated():
    "decorated"


@functools.cache
async def decorated_async():
    """decorated async"""


async def plain_async():
    """plain async"""


@functools.cache
class DecoratedClass:
    """decorated class"""


class Outer:
    def method(self):
        """method"""

    async def async_method(self):
        """async method"""

    @staticmethod
    @functools.cache
    async def stacked():
        '''stacked'''

    class Inner:
        """inner"""


def nested():
    def inner():
        """inner"""

    async def inner_async():
        """inner async"""

    return inner, inner_async


def implicit_concatenation():
    "one" "two"


def f_string(name):
    f"not a docstring {name}"


def bytes_literal():
    b"not a docstring"


def string_after_statement():
    value = 1
    "not a docstring"
    return value


def string_then_code():
    """doc"""
    return 1


def semicolon():
    "doc"; return 1


def number_first():
    1


def parenthesised():
    ("parenthesised")


def raw_and_prefix():
    r"raw"


def only_pass():
    pass


match 1:
    case 1:
        "not a docstring in a case"


if True:
    "not a docstring in an if"
