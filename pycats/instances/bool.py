"""
    Type class instances for Python bools.
"""
from pycats import (
    instance,
    Semigroup,
    Monoid
)


@instance(Semigroup, bool)
class BoolSemigroup:

    def combine(self, other):
        return self and other


@instance(Monoid, bool)
class BoolMonoid:

    @classmethod
    def unit(cls):
        return cls()
