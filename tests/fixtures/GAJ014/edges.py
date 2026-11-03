import os
from typing import Annotated, ClassVar, Final
import typing
import typing_extensions

A = 1
B: int = 1
C: Final = 1
D: Final[int] = 1
E: typing.Final = 1
F: typing.Final[int] = 1
G: typing_extensions.Final[int] = 1
H: "Final" = 1
I: Annotated[int, 1] = 1
J: Annotated[Final[int], 1] = 1
K: ClassVar[int] = 1
L: Final[Final[int]] = 1
M: int
N: Final
O, P = 1, 2
Q = R = 1
S = (T := 1)
_PRIVATE = 1
__dunder__ = 1
__a__b = 1
_ = 1
____ = 1
__x__ = 1
U = f"{A}"
V = lambda: 1
W: Final = lambda: 1
X = Y = Z = 1
[a, b] = [1, 2]
os.environ["K"] = "v"
os.name = "x"
counter = 0
counter += 1


def function():
    local = 1
    return local


async def async_function():
    local: int = 1
    return local


class Holder:
    member = 1
    other: int = 1


if True:
    CONDITIONAL = 1
    typed: int = 1

for loop in range(3):
    pass

with open(os.devnull) as handle:
    pass

match 1:
    case 1:
        matched = 1

try:
    pass
except OSError as error:
    pass
