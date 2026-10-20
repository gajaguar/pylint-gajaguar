import functools


@functools.cache
def decorated(_unused, _used):
    return _used


@functools.cache
async def decorated_async(_unused, *, _kw, _kw_used):
    return _kw_used


async def plain_async(_unused):
    pass


def positional_only(_a, /, _b, *_args, _c, **_kwargs):
    return _b


def keyword_only(*, _a, _b):
    return _a


def defaults(_a=1, _b=2, *, _c=3):
    return _b


def lambda_use(_a, _b):
    return lambda: _a


def lambda_param(_a):
    return lambda _a: 1


def nested_use(_a, _b):
    def inner():
        return _b

    return inner


def nested_shadow(_a):
    def inner(_a):
        return _a

    return inner


def f_string_use(_a, _b):
    return f"{_a}"


def f_string_format_spec(_a, _w):
    return f"{1:{_w}}"


def deleted(_a):
    del _a


def stored(_a):
    _a = 1


def augmented(_a):
    _a += 1


def used_in_decorator(_a):
    @functools.partial(print, _a)
    def inner():
        pass

    return inner


def used_in_annotation(_a: int, _b: "_a") -> _a:
    pass


def used_in_default(_a, _b=_a if False else 0):
    pass


def match_subject(_a, _b):
    match _a:
        case 1:
            pass


def match_capture(_a, _b):
    match _b:
        case [_a, _c]:
            pass


class Holder:
    def method(self, _a, _b):
        return _b

    @classmethod
    def build(cls, _a):
        pass

    @staticmethod
    async def static_async(_a):
        pass
