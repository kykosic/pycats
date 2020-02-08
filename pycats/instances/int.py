"""
    Type class instances for Python ints.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid
)


@instance(Semigroup, int)
class IntSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, int)
class IntMonoid:

    @classmethod
    def unit(cls):
        return cls()
