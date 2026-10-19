def test_custom_markers():
    # Given
    value = 1
    # When
    result = value
    # Then
    assert result == 1


def test_default_markers_are_extra():
    # Arrange
    # Act
    # Assert
    assert True


def test_explained():
    # Given
    value = 1  # explained
    assert value
