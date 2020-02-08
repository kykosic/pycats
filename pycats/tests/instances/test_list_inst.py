import pytest

import pycats.instances  # noqa: F401


def test_semigroup():
    a = [1, 2]
    b = [3, 4]

    actual = a.combine(b)
    expected = [1, 2, 3, 4]
    assert actual == expected
    actual = a + b
    assert actual == expected


def test_monoid():
    actual = list.unit()
    expected = list()
    assert actual == expected


def test_functor():
    a = [1, 2, 3]

    actual = a.map(lambda x: x + 2)
    expected = [3, 4, 5]
    assert actual == expected


def test_applicative_ap():
    a = [1, 2]

    fns = [lambda x: x + 2, lambda x: x - 1]
    actual = fns.ap(a)
    expected = [3, 1]
    assert actual == expected

    fns = [lambda x: x + 1 for _ in range(3)]
    with pytest.raises(TypeError):
        fns.ap(a)


def test_applicative_pure():
    actual = list.pure(1)
    expected = [1]
    assert actual == expected


def test_monad_flatten():
    a = [[1, 2], [3, 4]]
    actual = a.flatten()
    expected = [1, 2, 3, 4]
    assert actual == expected


def test_monad_flat_map():
    a = [1, 2]
    actual = a.flat_map(lambda x: [x - 1])
    expected = [0, 1]
    assert actual == expected
