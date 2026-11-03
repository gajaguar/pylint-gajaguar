import os

GOOD = 1
GOOD_2 = 2
_PRIVATE = 3
__dunder__ = 4
_ = 5
lower = 6
Mixed = 7
_lower = 8
__DOUBLE = 9
camelCase: int = 10
BARE: int
FIRST, second = 1, 2
(THIRD, fourth) = 3, 4
chained = OTHER = 5

for index in range(3):
    pass

with open(os.devnull) as handle:
    pass

try:
    pass
except OSError as error:
    pass

if (walrus := 1):
    pass

values = [item for item in range(3)]


def function(argument):
    local = 1
    return local


class Holder:
    member = 1


counter = 0
counter += 1
