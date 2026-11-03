import functools


def with_doc():
    """Docstring."""
    return 1


def without_doc():
    # comment only
    return 1


async def async_with_doc():
    "single quoted"


class WithDoc:
    """Class docstring."""

    def method(self):
        """Method docstring."""

    def plain(self):
        x = """not a docstring"""
        return x


class Plain:
    value = 1


@functools.cache
def decorated():
    """Decorated docstring."""


def second_statement():
    value = 1
    """Not the docstring."""
    return value


def concatenated():
    """First part """ """second part"""


def bytes_first():
    b"bytes are not docs"


def formatted_first():
    f"{1}"


def nested():
    def inner():
        """Inner docstring."""

    return inner
