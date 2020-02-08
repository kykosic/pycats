"""
    Type class instances for Python Ints.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid
)


@instance(Semigroup, str)
class StrSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, str)
class StrMonoid:

    @classmethod
    def unit(cls):
        return cls()
