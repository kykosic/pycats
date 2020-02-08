"""
    Applicative type class.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass
from pycats.functor import Functor


@typeclass
class Applicative(Functor, ABC):
    """ Extends `Functor`, provides `ap` and `pure` methods.

    Signatures for `Applicative[F[_]]`:
        - `F[A -> B].ap(objs: F[A]) -> F[B]`
        - `F[A].pure(obj: A) -> F[A]`

    """

    @abstractmethod
    def ap(self, obj):
        pass

    @classmethod
    @abstractmethod
    def pure(cls, obj):
        pass
