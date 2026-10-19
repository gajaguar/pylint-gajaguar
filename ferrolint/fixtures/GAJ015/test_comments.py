import pytest


def test_markers_only():
    # Arrange
    value = 1
    # Act
    result = value
    # Assert
    assert result == 1


def test_marker_in_trailing_comment():
    # Arrange
    value = 1
    assert value  # Assert


def test_explanatory():
    # Arrange
    value = 1  # the value under test
    # compute the result
    result = value
    assert result == 1


def test_marker_lookalikes():
    #Arrange
    # Arrange: set up
    #   Act
    # arrange
    # Assert  # and more
    assert True


def test_pragmas_are_allowed():
    value = 1  # noqa: F841
    other = 2  # pylint: disable=unused-variable
    third = 3  # type: int
    fourth = 4  # mypy: ignore
    # fmt: off
    fifth = [1,2]
    # fmt: on
    sixth = 6  # ruff: ignore[F841]
    assert value, other


def test_pragma_lookalikes():
    value = 1  #noqa
    other = 2  # NOQA
    third = 3  # Noqa: F841
    fourth = 4  # pylint : disable=foo
    assert value, other


def test_def_line_comment():  # explains the test
    assert True


@pytest.mark.parametrize("value", [1, 2])  # decorators are not the body
def test_decorated(value):
    assert value


def test_multiline_call():
    assert dict(
        a=1,  # first key
        # second key
        b=2,
    )


def test_hash_in_string():
    text = "# explain"
    other = """
    # not a comment
    """
    assert text, other


def test_after_last_statement():
    assert True
    # outside the body


def test_outer():
    # outer note
    def test_inner():
        # inner note
        assert True

    assert test_inner


def test_empty_comment():
    #
    assert True


async def test_async_explained():
    # await the thing
    assert True


class TestHolder:
    def test_method_explained(self):
        # explain
        assert True

    # a note between methods
    def test_method_clean(self):
        # Arrange
        assert True

    @staticmethod
    def test_static_explained():
        assert True  # still explained


def test_tabbed():
	# tab indented
	assert True


def helper_not_a_test():
    # explained, but not a test
    return 1
