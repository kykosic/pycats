"""
    Monad type class.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass
from pycats.applicative import Applicative


@typeclass
class Monad(Applicative, ABC):
    """ Extends `Applicative`, provides `flatten` and `flat_map` methods.

    Signatures for `Monad[F[_]]`:
        - `F[F[A]].flatten() -> F[A]`
        - `F[A].flat_map(func: A -> F[B]) -> F[B]`
    """

    @abstractmethod
    def flatten(self):
        pass

    def flat_map(self, func):
        return self.map(func).flatten()
