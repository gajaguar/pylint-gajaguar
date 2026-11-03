import functools


@functools.cache
# Arrange
# Act
# Assert
def test_markers_between_decorator_and_def():
    assert True


@functools.cache

# Arrange
def test_blank_between_decorator_and_def():
    # Act
    # Assert
    assert True


@functools.partial(
    print,
    1,
)
# Arrange
async def test_multiline_decorator():
    assert True


@functools.cache
# Act
@functools.cache
# Arrange
def test_comments_between_decorators():
    # Assert
    assert True
