def test_no_blank():
    # Arrange
    value = 1
    # Assert
    assert value


def test_blank_in_middle():
    value = 1

    assert value


def test_two_blanks():
    value = 1

    other = 2

    assert value, other


def test_blank_in_string():
    text = """first

    second"""
    assert text


def helper_with_blank():
    value = 1

    return value


async def test_async_blank():
    value = 1

    assert value


class TestHolder:
    def test_method_blank(self):
        value = 1

        assert value

    @staticmethod
    def test_decorated_blank():
        value = 1

        assert value
