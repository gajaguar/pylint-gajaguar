import functools
import pytest


@functools.cache
def test_decorated():
    assert response["count"] == 3


@pytest.mark.parametrize("value", [1, 2])
@functools.cache
async def test_stacked_async(value):
    assert reply["ok"] is True


def test_f_string():
    assert f"{x}" == data["a"]


def test_match(value):
    match value:
        case 1:
            assert response["count"] == 3
        case _:
            assert response == {}


def test_nested_function():
    def inner():
        assert nested["k"] == 1

    assert inner


def test_assert_with_message():
    assert response["count"] == 3, "message"


def test_whole_in_other_assert_of_nested_function():
    def inner():
        assert response == {}

    assert response["count"] == 3


def test_chained_subscript_on_right():
    assert 3 == response["count"]


def test_both_sides():
    assert left["a"] == right["a"]


def test_in_operator():
    assert "k" in response["items"]


def test_is_comparison():
    assert response["ok"] is True


def test_slice():
    assert response[1:2] == [1]


def test_multi_line():
    assert (
        response["count"]
        == 3
    )


class TestHolder:
    @functools.cache
    async def test_method(self):
        assert reply["ok"] == 1

    def test_whole(self):
        assert reply["ok"] == 1
        assert reply == {}
