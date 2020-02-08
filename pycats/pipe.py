"""
    Pipe type class.

    It can be used to fluently sequence computations on any object,
    but is especially useful to transform lazily evaluated data, such
    as Python generators.

    Users of R will find it similar to the dplyr `%>%` operator.
"""
from abc import ABC, abstractmethod

from pycats.core import typeclass


@typeclass
class Pipe(ABC):
    """ Provides `pipe` method.

    Signatures for `Pipe[A]`:
        - `A.pipe(func: A -> B) -> B`

    """

    @abstractmethod
    def pipe(self, func):
        pass
