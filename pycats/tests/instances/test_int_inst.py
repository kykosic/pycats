import pycats.instances  # noqa: F401


def test_semigroup():
    a = 1
    b = 2

    actual = a.combine(b)
    expected = 3
    assert actual == expected
    assert isinstance(actual, int)
    actual = a + b
    assert actual == expected


def test_monoid():
    actual = int.unit()
    expected = 0
    assert actual == expected
    assert isinstance(actual, int)
