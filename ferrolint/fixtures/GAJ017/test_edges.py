import functools
import pytest


@functools.cache
def test_decorated_mock():
    assert True


@pytest.mark.parametrize("value", [1, 2])
@functools.cache
async def test_stacked_async_patch(value):
    assert value


async def test_async_called():
    assert True


def test_Mock_upper():
    assert True


def test_MOCK_RETURN_VALUE():
    assert True


def test_stubbed():
    assert True


def test_impl_detail():
    assert True


def test_implementation():
    assert True


def test_privately():
    assert True


def test_return_value_is_set():
    assert True


def test_returnvalue():
    assert True


def test_call_count_calls():
    assert True


def test_spy_and_stub():
    assert True


def test_double__underscore__mock():
    assert True


def test_digits_mock2():
    assert True


def test_mock_2():
    assert True


def test_café_mock():
    assert True


def test_nested_function():
    def test_inner_mock():
        pass

    assert test_inner_mock


class TestHolder:
    @functools.cache
    async def test_method_mock(self):
        assert True

    def test_clean(self):
        assert True

    class TestNested:
        def test_nested_spy(self):
            assert True
