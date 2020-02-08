import pytest

from pycats.data import Result, Ok, Err


@pytest.mark.parametrize("obj", [
    1,
    1.0,
    False,
    "cat",
    [1, 2, 3]
])
def test_ok(obj):
    ok = Ok(obj)

    assert ok.value == obj

    a_obj = ok.match(
        ok=lambda x: x,
        err=None
    )
    assert a_obj == obj

    resp = ok.match(
        ok=12345,
        err=None
    )
    assert resp == 12345


def test_err():
    msg = "This is a type error."
    exc = TypeError(msg)
    err = Err(exc)

    obj = err.match(
        ok=None,
        err=lambda e: e
    )
    assert obj == exc

    with pytest.raises(TypeError):
        err.unwrap()

    err2 = Err(msg)
    obj2 = err.match(
        ok=None,
        err=lambda e: str(e)
    )
    assert obj2 == msg

    obj3 = err2.unwrap()
    assert obj3 == msg

    obj4 = err.match(
        ok=None,
        err=1234
    )
    assert obj4 == 1234


def test_result():
    with pytest.raises(TypeError):
        Result()

    @Result.wrap
    def good_fn():
        return 123

    obj = good_fn()
    assert isinstance(obj, Ok)
    assert obj.unwrap() == 123

    @Result.wrap
    def bad_fn():
        raise ValueError("Bad thing!")

    obj = bad_fn()
    assert isinstance(obj, Err)
    with pytest.raises(ValueError, match="Bad thing!"):
        obj.unwrap()
