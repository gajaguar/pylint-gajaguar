def test_custom_markers():
    # Given
    value = 1
    # When
    result = value
    # Then
    assert result == 1


def test_default_markers_do_not_count():
    # Arrange
    # Act
    # Assert
    assert True


def test_missing_then():
    # Given
    # When
    assert True
