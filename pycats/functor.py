"""
    Functor type class.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass


@typeclass
class Functor(ABC):
    """ Provides the `map` method.

    Signatures for `Functor[F[_]]`:
        - `F[A].map[B](func: A -> B) -> F[B]`

    """

    @abstractmethod
    def map(self, func):
        pass
