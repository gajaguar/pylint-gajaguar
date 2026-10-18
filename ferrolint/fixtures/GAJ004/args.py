def unused_underscore(_value):
    return 1


def used_underscore(_value):
    return _value


def plain(value):
    return 1


def only_underscore(_):
    return 1


def dunder_prefix(__value):
    return 1


def method_like(self, _unused, _used):
    return _used


def keyword_only(*, _flag):
    return 1


def positional_only(_pos, /, other):
    return other


def with_default(_value=1):
    return 1


def star_args(*_args, **_kwargs):
    return 1


def deleted(_value):
    del _value


def used_in_nested(_value):
    def inner():
        return _value

    return inner


def used_in_default(_value, other=_value):
    return other


def used_in_annotation(_value, other: _value):
    return other


def stored_only(_value):
    _value = 1
    return _value


async def coroutine(_value):
    return 1


class Holder:
    def method(self, _value):
        return 1

    @classmethod
    def build(cls, _value):
        return cls


handler = lambda _value: 1
