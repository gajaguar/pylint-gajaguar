def test_field_without_whole_object():
    assert response["count"] == 3


def test_whole_object_suppresses():
    assert response["count"] == 3
    assert response == {"count": 3}


def test_plain_assertion():
    assert value == 3


def test_nested_subscript():
    assert data["a"]["b"] == 1


def test_several_names_sorted():
    assert zeta["k"] == 1
    assert alpha["k"] == 2


def test_whole_on_the_right():
    assert items[0] == 1
    assert 1 != items


def test_chained_comparison():
    assert low[0] < mid < high[1]


def test_attribute_root_is_ignored():
    assert obj.items["k"] == 1


def test_call_root_is_ignored():
    assert load()["k"] == 1


def test_negated_compare_is_ignored():
    assert not (response["count"] == 3)


def test_bare_subscript_is_ignored():
    assert response["count"]


async def test_async_fires():
    assert reply["ok"] is True


@decorate
def test_decorated():
    assert body["id"] == 1


def test_nested_function_assertion():
    def inner():
        assert inner_value["k"] == 1

    inner()


def test_other_whole_object_does_not_suppress():
    assert first["k"] == 1
    assert second == {}
