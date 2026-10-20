import functools
import pytest


@functools.cache  # decorator comment
def test_decorated():
    # Arrange
    assert True  # explains


@pytest.mark.parametrize("value", [1, 2])
# comment between decorators
@functools.cache
async def test_stacked_async(value):  # def line
    # why
    assert value


async def test_async():
    # Act
    # Assert
    await x  # awaiting


def test_f_string():
    name = "x"
    text = f"# not a comment {name}"  # real comment
    assert text


def test_hash_in_strings():
    text = "# Arrange"
    other = '''# not a comment
# nor this'''
    assert text, other  # trailing


def test_match(value):
    # Arrange
    match value:  # subject
        # case comment
        case 1:  # one
            pass
        case _:
            pass  # Assert


def test_nested_function():
    def inner():
        # inner comment
        pass

    return inner  # outer


def test_comment_after_body():
    assert True
    # trailing comment on its own line


def test_continuation():
    value = (
        1  # first
        + 2  # second
    )
    assert value


def test_pragma_variants():
    a = 1  # noqa
    b = 2  # type: ignore
    c = 3  # pylint: disable=x
    d = 4  # ruff: noqa
    e = 5  # mypy: ignore-errors
    f = 6  # fmt: skip
    assert (a, b, c, d, e, f)


class TestHolder:
    # class comment
    @functools.cache
    # between decorator and def
    async def test_method(self):  # def line
        # method comment
        assert True

    # before next
    def test_second(self):
        # Arrange
        assert True


# module comment between tests
def test_after_module_comment():
    assert True  # trailing
