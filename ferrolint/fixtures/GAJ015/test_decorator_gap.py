import functools


@functools.cache
# comment between
def test_one():
    assert True


@functools.cache
# Arrange
@functools.cache
# comment between decorators
async def test_two():
    assert True


@functools.partial(
    print,  # inside the decorator
    1,
)
# after a multi-line decorator
def test_three():
    assert True
