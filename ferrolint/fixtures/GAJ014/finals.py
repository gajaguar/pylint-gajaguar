import typing
from typing import Final

PLAIN = 1
ANNOTATED: int = 1
FINAL: Final = 1
FINAL_SUBSCRIPT: Final[int] = 1
FINAL_ATTRIBUTE: typing.Final = 1
FINAL_ATTRIBUTE_SUBSCRIPT: typing.Final[int] = 1
__all__ = ["PLAIN"]
__version__ = "1"
_ = 1
lower = 2
FIRST, SECOND = 1, 2
CHAINED = OTHER = 3
BARE: int
attribute.value = 4
items[0] = 5

if PLAIN:
    CONDITIONAL = 6

for index in range(3):
    LOOPED = index


def function():
    local = 1
    return local


class Holder:
    member = 1
