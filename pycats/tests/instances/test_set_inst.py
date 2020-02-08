import pycats.instances  # noqa: F401


def test_semigroup():
    a = {1, 2}
    b = {2, 4}

    actual = a.combine(b)
    expected = {1, 2, 4}
    assert actual == expected


def test_monoid():
    actual = list.unit()
    expected = list()
    assert actual == expected


def test_functor():
    a = {1, 2, 3}

    actual = a.map(lambda x: x + 2)
    expected = {3, 4, 5}
    assert actual == expected
