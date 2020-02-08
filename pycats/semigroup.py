"""

    Semigroup type class.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass


@typeclass
class Semigroup(ABC):
    """ Provides the `combine` method.

    Signatures for `Semigroup[A]`:
        - `A.combine(other: A) -> A`

    """

    @abstractmethod
    def combine(self, other):
        pass
