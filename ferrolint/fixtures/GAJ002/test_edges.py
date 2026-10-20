import functools
import pytest


@functools.cache
def test_decorated():
    assert True


@pytest.mark.parametrize("value", [1, 2])
@functools.cache
async def test_stacked_async(value):
    assert value


async def test_async_complete():
    # Arrange
    value = 1
    # Act
    result = await value
    # Assert
    assert result


def test_f_string():
    name = "x"
    # Arrange
    print(f"# Act {name}")
    assert f"# Assert {name}"


def test_markers_in_string():
    text = "# Arrange # Act # Assert"
    assert text


def test_match(value):
    # Arrange
    match value:
        # Act
        case 1:
            pass
        # Assert
        case _:
            pass


def test_nested_function():
    def test_inner():
        pass

    # Arrange
    # Act
    # Assert
    assert test_inner


class TestHolder:
    @functools.cache
    async def test_decorated_async_method(self):
        assert True

    class TestNested:
        def test_nested_class_method(self):
            # Arrange
            # Act
            # Assert
            assert True


test_lambda = lambda: None
