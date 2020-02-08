import pycats.instances  # noqa: F401


def test_semigroup():
    a = True
    b = True
    actual = a.combine(b)
    expected = True
    assert actual == expected
    assert isinstance(actual, bool)

    a = True
    b = False
    actual = a.combine(b)
    expected = False
    assert actual == expected
    assert isinstance(actual, bool)

    a = False
    b = True
    actual = a.combine(b)
    expected = False
    assert actual == expected
    assert isinstance(actual, bool)

    a = False
    b = False
    actual = a.combine(b)
    expected = False
    assert actual == expected
    assert isinstance(actual, bool)


def test_monoid():
    actual = bool.unit()
    expected = False
    assert actual == expected
    assert isinstance(actual, bool)
