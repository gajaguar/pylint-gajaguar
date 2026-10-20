import functools


@functools.cache

def test_blank_between_decorator_and_def():
    assert True


@functools.cache
# comment

def test_blank_after_comment():
    assert True


@functools.partial(
    print,
    1,
)

async def test_multiline_decorator():
    assert True


@functools.cache

@functools.cache
def test_blank_between_decorators():
    value = 1

    assert value
