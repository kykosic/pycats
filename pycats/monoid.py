"""
    Monoid type class.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass
from pycats.semigroup import Semigroup


@typeclass
class Monoid(Semigroup, ABC):
    """ Extends `Semigroup`, provides `unit` method.

    Signatures for `Monoid[A]`:
        - `A.unit() -> A`

    """

    @classmethod
    @abstractmethod
    def unit(cls):
        pass
