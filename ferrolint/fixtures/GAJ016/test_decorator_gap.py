import functools


@functools.cache
# comment between

def test_partial():
    assert response["count"] == 3


@functools.cache
@functools.cache

async def test_partial_async():
    assert reply["ok"] is True
