from typing import Final

LITERAL = {"a", "b"}
CALL = set()
FROM_ITER = set([1, 2])
COMPREHENSION = {x for x in range(3)}
ATTRIBUTE = builtins.set()
ANNOTATED: set[str] = {"a"}
ANNOTATED_FINAL: Final[set[str]] = {"a"}
CHAINED = OTHER = {1}
FROZEN = frozenset({"a"})
DICT = {"a": 1}
LIST = [1, 2]
EMPTY_DICT = {}
BARE_ANNOTATION: set[str]

if True:
    CONDITIONAL = {1}

for index in range(3):
    LOOPED = {index}


def function():
    local = {1}
    return local


class Holder:
    members = {1}
