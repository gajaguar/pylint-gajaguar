import os
from . import a
from .b import c
from .. import d
from ..e import f
from ... import g
from .... import h
from .i.j import k
from os import path
from os.path import join as j, sep
from . import (
    multi,
    line,
)
from .l import (m as n,
                o)
from .p import *


def function():
    from . import inner


async def async_function():
    from .. import inner_async


class Holder:
    from . import member


if True:
    from .q import r
