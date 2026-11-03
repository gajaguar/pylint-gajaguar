command = ["go", "north"]

match command:
    case [action, *rest]:
        pass
    case [_, *_]:
        pass
    case {"key": value, **others}:
        pass
    case {"key": GOOD_VALUE, **OTHERS}:
        pass
    case str() as text:
        pass
    case int(CODE) | float(CODE):
        pass
    case Point(x=px, y=PY) as POINT:
        pass
    case ([first, second] as pair) | (pair, second):
        pass
    case [
        1,
        multi,
    ] as spread:
        pass
    case {
        "a": 1,
        **tail,
    }:
        pass
    case [
        1,
        *rest_multi,
    ]:
        pass
    case _:
        pass


def function(argument):
    match argument:
        case [local, *rest]:
            return local, rest
        case {"key": value}:
            return value


class Holder:
    match command:
        case [member]:
            pass
