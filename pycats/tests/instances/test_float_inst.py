import pycats.instances  # noqa: F401


def test_semigroup():
    a = 1.0
    b = 2.0

    actual = a.combine(b)
    expected = 3.0
    assert actual == expected
    assert isinstance(actual, float)
    actual = a + b
    assert actual == expected


def test_monoid():
    actual = float.unit()
    expected = 0.0
    assert actual == expected
    assert isinstance(actual, float)
