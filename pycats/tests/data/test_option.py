import pytest

from pycats.data import Option, Some, Nil


@pytest.mark.parametrize("obj", [
    1,
    1.0,
    False,
    "cat",
    [1, 2, 3]
])
def test_some(obj):
    some = Some(obj)

    assert some.value == obj

    a_obj = some.match(
        some=lambda x: x,
        nil=None
    )
    assert a_obj == obj

    resp = some.match(
        some=12345,
        nil=None
    )
    assert resp == 12345


def test_nil():
    nil = Nil()

    obj = nil.match(
        some=None,
        nil=123
    )
    assert obj == 123

    n_obj = nil.unwrap()
    assert n_obj is None


def test_option():
    with pytest.raises(TypeError):
        Option()
