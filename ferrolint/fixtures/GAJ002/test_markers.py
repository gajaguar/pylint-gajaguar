def test_complete():
    # Arrange
    value = 1
    # Act
    result = value
    # Assert
    assert result == 1


def test_missing_all():
    assert True


def test_missing_assert():
    # Arrange
    value = 1
    # Act
    value += 1


def test_marker_in_trailing_comment():
    value = 1  # Arrange
    # Act
    # Assert
    assert value


def helper_without_markers():
    return 1


async def test_async_missing():
    assert True


class TestHolder:
    def test_method_missing(self):
        assert True

    @staticmethod
    def test_decorated_missing():
        assert True

    # Arrange Act Assert in a class comment does not count
    def test_marker_text_without_hash(self):
        text = "Arrange Act Assert"
        assert text
