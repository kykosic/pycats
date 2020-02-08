import pycats.instances  # noqa: F401
from pycats.data import Option, Some, Nil


def test_semigroup():
    a = Some(1)
    b = Some(2)
    n = Nil()

    actual = a.combine(b)
    expected = Some(3)
    assert actual == expected
    actual = a + b
    assert actual == expected

    actual = a.combine(n)
    expected = n
    assert actual == expected

    actual = n.combine(b)
    expected = n
    assert actual == expected

    actual = n.combine(n)
    expected = n
    assert actual == expected


def test_monoid():
    assert Option.unit() == Nil()
    assert Some.unit() == Nil()
    assert Nil.unit() == Nil()


def test_functor():
    a = Some(2)
    n = Nil()

    actual = a.map(lambda x: x + 2)
    expected = Some(4)
    assert actual == expected

    actual = n.map(lambda x: x + 2)
    expected = Nil()
    assert actual == expected


def test_applicative_ap():
    a = Some(3)
    n = Nil()

    fn = Some(lambda x: x - 1)
    actual = fn.ap(a)
    expected = Some(2)
    assert actual == expected

    actual = fn.ap(n)
    expected = Nil()
    assert actual == expected

    fn = Nil()
    actual = fn.ap(a)
    expected = Nil()
    assert actual == expected


def test_applicative_pure():
    actual = Option.pure(1)
    expected = Some(1)
    assert actual == expected


def test_monad_flatten():
    a = Some(Some(3))
    actual = a.flatten()
    expected = Some(3)
    assert actual == expected

    a = Some(Nil())
    actual = a.flatten()
    expected = Nil()
    assert actual == expected

    a = Nil()
    actual = a.flatten()
    expected = Nil()
    assert actual == expected


def test_monad_flat_map():
    a = Some(2)
    actual = a.flat_map(lambda x: Some(x + 3))
    expected = Some(5)
    assert actual == expected

    actual = a.flat_map(lambda _: Nil())
    expected = Nil()
    assert actual == expected

    n = Nil()
    actual = n.flat_map(lambda x: Some(x + 1))
    expected = Nil()
    assert actual == expected
