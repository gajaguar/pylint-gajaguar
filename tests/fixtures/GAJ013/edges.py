from typing import Final

A = {1}
B: set[int] = {1}
C: Final = {1}
D: Final[set[int]] = {1}
E = set()
F = set([1])
G = {i for i in range(3)}
H = {i: i for i in range(3)}
I = {}
J = frozenset({1})
K = {*[1]}
L, M = {1}, {2}
N = O = {1}
P: set[int]
Q = (R := {1})
S = f"{ {1} }"
T = [{1}]
U = {1} | {2}
V = set(())
W = builtins.set()
X = os.set()
Y = lambda: {1}
Z = None if False else {1}


def function():
    inner = {1}
    return inner


async def async_function():
    inner: set[int] = {1}
    return inner


class Holder:
    member = {1}


if True:
    CONDITIONAL = {1}

match 1:
    case 1:
        MATCHED = {1}
