import functools


@functools.cache
# comment between

def test_mock_name():
    assert True


@functools.partial(
    print,
    1,
)

async def test_stub_name():
    assert True
