import contextlib
import functools


@functools.cache
def decorated():
    try:
        pass
    except OSError:
        pass


async def async_function():
    try:
        pass
    except OSError:
        pass
    try:
        pass
    except (OSError, ValueError):
        pass


def multiple_handlers():
    try:
        pass
    except OSError:
        pass
    except ValueError:
        pass


def mixed_handlers():
    try:
        pass
    except OSError:
        pass
    except ValueError:
        print()


def bare_handler():
    try:
        pass
    except:
        pass


def exception_group():
    try:
        pass
    except* OSError:
        pass


def with_else():
    try:
        pass
    except OSError:
        pass
    else:
        print()


def with_finally():
    try:
        pass
    except OSError:
        pass
    finally:
        print()


def as_name():
    try:
        pass
    except OSError as error:
        pass


def two_passes():
    try:
        pass
    except OSError:
        pass
        pass


def pass_after_docstring_like():
    try:
        pass
    except OSError:
        "text"
        pass


def match_in_try(value):
    try:
        match value:
            case 1:
                pass
    except OSError:
        pass


def f_string_in_try(name):
    try:
        print(f"{name}")
    except OSError:
        pass


def nested():
    try:
        try:
            pass
        except KeyError:
            pass
    except OSError:
        pass


class Holder:
    try:
        pass
    except OSError:
        pass


try:
    pass
except OSError:
    pass


with contextlib.suppress(OSError):
    pass
