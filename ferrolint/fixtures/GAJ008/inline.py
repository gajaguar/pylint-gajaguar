import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import json
    from collections import abc

if os.name:
    import sys


def function():
    import re
    from os import path as p, sep
    import xml.dom as dom, string
    return re, p, sep, dom, string


async def coroutine():
    import asyncio
    return asyncio


def guarded():
    if TYPE_CHECKING:
        from decimal import Decimal
        import fractions
    else:
        from datetime import date
    return Decimal, date


def guarded_attribute():
    if typing.TYPE_CHECKING:
        from uuid import UUID
    return UUID


def elif_branch(flag):
    if flag:
        pass
    elif TYPE_CHECKING:
        from copy import copy
    return copy


class Holder:
    import random
    from math import pi


def outer():
    def inner():
        import heapq
        return heapq

    return inner
