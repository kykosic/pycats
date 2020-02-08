import pytest

import pycats.instances  # noqa: F401
from pycats.data import generator


def assert_gen_equal(gen_a, gen_b):
    """ Helper function to determine if two generators are equal. """
    assert isinstance(gen_a, generator)
    assert isinstance(gen_b, generator)
    list_a = list(gen_a)
    list_b = list(gen_b)
    assert list_a == list_b


def test_semigroup():
    a = (x for x in [1, 2])
    b = (x for x in [3, 4])
    actual = a.combine(b)
    expected = (x for x in (1, 2, 3, 4))
    assert_gen_equal(actual, expected)


def test_monoid():
    actual = generator.unit()
    expected = (_ for _ in range(0))
    assert_gen_equal(actual, expected)


def test_functor():
    a = (x for x in [1, 2, 3])
    actual = a.map(lambda x: x + 2)
    expected = (x for x in [3, 4, 5])
    assert_gen_equal(actual, expected)


def test_applicative_ap():
    a = (x for x in [1, 2])
    fns = (f for f in [lambda x: x + 2, lambda x: x - 1])
    actual = fns.ap(a)
    expected = (x for x in [3, 1])
    assert_gen_equal(actual, expected)

    a = (x for x in [1, 2])
    fns = (lambda x: x + 1 for _ in range(3))
    with pytest.raises(TypeError):
        list(fns.ap(a))

    a = (x for x in [1, 2])
    fns = generator.unit()
    with pytest.raises(TypeError):
        list(fns.ap(a))


def test_applicative_pure():
    actual = generator.pure(1)
    expected = (x for x in [1])
    assert_gen_equal(actual, expected)


def test_monad_flatten():
    a = (x for x in [(y for y in [1, 2]), (y for y in [3, 4])])
    actual = a.flatten()
    expected = (x for x in [1, 2, 3, 4])
    assert_gen_equal(actual, expected)


def test_monad_flat_map():
    a = (x for x in [1, 2])

    def minus_one(x):
        yield x - 1

    actual = a.flat_map(minus_one)
    expected = (x for x in [0, 1])
    assert_gen_equal(actual, expected)


def test_pipe():
    a = (x for x in range(4))

    def pair_batch(gen):
        pair = list()
        for x in gen:
            pair.append(x)
            if len(pair) == 2:
                yield pair
                pair = list()

    actual = pair_batch(a)
    expected = (x for x in [[0, 1], [2, 3]])
    assert_gen_equal(actual, expected)
