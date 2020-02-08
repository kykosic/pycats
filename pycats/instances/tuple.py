"""
    Type class instances for Python tuple.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid,
    Functor,
    Applicative,
    Monad
)


@instance(Semigroup, tuple)
class TupleSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, tuple)
class TupleMonoid:

    @classmethod
    def unit(cls):
        return cls()


@instance(Functor, tuple)
class TupleFunctor:

    def map(self, func):
        return tuple(func(x) for x in self)


@instance(Applicative, tuple)
class TupleApplicative:

    def ap(self, obj):
        n_funcs = len(self)
        n_objs = len(obj)
        if n_funcs != n_objs:
            raise TypeError(f"Incompatible lengths, ap {n_funcs} to {n_objs}")
        return tuple(fn(x) for (fn, x) in zip(self, obj))

    @classmethod
    def pure(cls, obj):
        return (obj,)


@instance(Monad, tuple)
class TupleMonad:

    def flatten(self):
        return tuple(x for ls in self for x in ls)
