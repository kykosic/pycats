"""
    Type class instances for Python sets.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid,
    Functor
)


@instance(Semigroup, set)
class SetSemigroup:

    def combine(self, other):
        return self.union(other)


@instance(Monoid, set)
class SetMonoid:

    @classmethod
    def unit(cls):
        return cls()


@instance(Functor, set)
class SetFunctor:

    def map(self, func):
        return {func(x) for x in self}
