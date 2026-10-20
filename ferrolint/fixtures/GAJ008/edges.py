import functools


@functools.cache
def decorated():
    import os


@functools.cache
async def decorated_async():
    import sys


@functools.cache
@functools.cache
async def stacked_async():
    import json


async def plain_async():
    import re


def f_string():
    return f"{__import__('os')}"


def match_in_function(value):
    match value:
        case 1:
            import os
        case _:
            from os import path


def nested():
    def inner():
        import os

    async def inner_async():
        import os.path as p, sys

    return inner, inner_async


class Outer:
    import os

    def method(self):
        import os

    async def async_method(self):
        from . import sibling

    class Inner:
        from os import path as p, sep


lambda_import = lambda: __import__("os")


def conditional():
    if True:
        import os
    try:
        import json
    except ImportError:
        json = None
    with open("f"):
        from os import path
    for _ in range(1):
        import re
    while False:
        import sys


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import os


def type_checking():
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        import os
        from os import path
    else:
        from os import sep
    if not TYPE_CHECKING:
        from os import name
    import typing

    if typing.TYPE_CHECKING:
        from os import linesep
    elif True:
        from os import pathsep
    else:
        import os.path


@functools.cache
# comment between the decorator and the def

async def decorator_gap():
    import os
