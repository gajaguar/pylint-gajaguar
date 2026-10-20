import functools
import pytest


@functools.cache
def test_decorated_blank():
    value = 1

    assert value


@pytest.mark.parametrize("value", [1, 2])

@functools.cache
async def test_blank_between_decorators(value):
    assert value


async def test_async_blank():
    value = 1

    assert value


def test_blank_after_def():

    assert True


def test_blank_in_multiline_string():
    text = """a

b"""
    assert text


def test_blank_in_f_string():
    name = "x"
    text = f"""{name}

{name}"""
    assert text


def test_blank_in_match(value):
    match value:
        case 1:
            pass

        case _:
            pass


def test_trailing_blank():
    assert True



def test_no_blank():
    value = 1
    assert value


class TestHolder:
    @functools.cache
    async def test_method_blank(self):
        value = 1

        assert value

    def test_second_blank(self):
        value = 1
        assert value

        assert value

    class TestNested:
        def test_nested_blank(self):
            value = 1

            assert value


def test_nested_function_blank():
    def inner():
        pass

    assert inner
