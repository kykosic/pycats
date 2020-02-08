import pycats.instances  # noqa: F401


def test_semigroup():
    a = 'cat'
    b = 'dog'

    actual = a.combine(b)
    expected = 'catdog'
    assert actual == expected
    assert isinstance(actual, str)
    actual = a + b
    assert actual == expected


def test_monoid():
    actual = str.unit()
    expected = ''
    assert actual == expected
    assert isinstance(actual, str)
