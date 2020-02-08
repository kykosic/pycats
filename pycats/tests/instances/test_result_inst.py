import pycats.instances  # noqa: F401
from pycats.data import Result, Ok, Err


def assert_err_eq(err_a, err_b):
    """ Assert two exceptions are equal. """
    assert isinstance(err_a, Err)
    assert isinstance(err_b, Err)
    exc_a = err_a.value
    exc_b = err_b.value
    assert type(exc_a) == type(exc_b)
    assert exc_a.args == exc_b.args


def test_semigroup():
    a = Ok(3)
    b = Ok(4)
    e = Err(TypeError("Bad thing!"))

    actual = a.combine(b)
    expected = Ok(7)
    assert actual == expected
    actual = a + b
    assert actual == expected

    actual = a.combine(e)
    expected = e
    assert_err_eq(actual, expected)

    actual = e.combine(a)
    expected = e
    assert_err_eq(actual, expected)

    actual = e.combine(e)
    expected = e
    assert_err_eq(actual, expected)


def test_functor():
    a = Ok(3)
    e = Err(TypeError("Bad thing!"))

    actual = a.map(lambda x: x + 1)
    expected = Ok(4)
    assert actual == expected

    actual = e.map(lambda x: x + 1)
    expected = e
    assert_err_eq(actual, expected)


def test_applicative_ap():
    a = Ok(2)
    e = Err(TypeError("Bad thing!"))

    fn = Ok(lambda x: x - 1)
    actual = fn.ap(a)
    expected = Ok(1)
    assert actual == expected

    actual = fn.ap(e)
    expected = e
    assert_err_eq(actual, expected)

    fn = Err(TypeError("Bad thing!"))
    actual = fn.ap(a)
    expected = fn
    assert_err_eq(actual, expected)


def test_applicative_pure():
    actual = Result.pure(1)
    expected = Ok(1)
    assert actual == expected


def test_monad_flatten():
    a = Ok(Ok(2))
    actual = a.flatten()
    expected = Ok(2)
    assert actual == expected

    a = Ok(Err(TypeError("Bad thing!")))
    actual = a.flatten()
    expected = Err(TypeError("Bad thing!"))
    assert_err_eq(actual, expected)

    a = Err(TypeError("Bad thing!"))
    actual = a.flatten()
    expected = a
    assert_err_eq(actual, expected)


def test_monad_flat_map():
    a = Ok(2)
    actual = a.flat_map(lambda x: Ok(x + 1))
    expected = Ok(3)
    assert actual == expected

    actual = a.flat_map(lambda _: Err(TypeError("Bad thing!")))
    expected = Err(TypeError("Bad thing!"))
    assert_err_eq(actual, expected)

    e = Err(TypeError("Bad thing!"))
    actual = e.flat_map(lambda x: Ok(x + 1))
    expected = e
    assert_err_eq(actual, expected)
