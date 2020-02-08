"""
    Type class instances for Python lists.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid,
    Functor,
    Applicative,
    Monad
)


@instance(Semigroup, list)
class ListSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, list)
class ListMonoid:

    @classmethod
    def unit(cls):
        return cls()


@instance(Functor, list)
class ListFunctor:

    def map(self, func):
        return [func(x) for x in self]


@instance(Applicative, list)
class ListApplicative:

    def ap(self, obj):
        n_funcs = len(self)
        n_objs = len(obj)
        if n_funcs != n_objs:
            raise TypeError(f"Incompatible lengths, ap {n_funcs} to {n_objs}")
        return [fn(x) for (fn, x) in zip(self, obj)]

    @classmethod
    def pure(cls, obj):
        return [obj]


@instance(Monad, list)
class ListMonad:

    def flatten(self):
        return [x for ls in self for x in ls]
