"""
    Type class instances for Python Floats.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid
)


@instance(Semigroup, float)
class FloatSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, float)
class FloatMonoid:

    @classmethod
    def unit(cls):
        return cls()
