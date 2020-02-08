"""
    Type class instances for the Result type.
"""
from pycats import (
    Result,
    Ok,
    Err,
    instance,
    Semigroup,
    Functor,
    Applicative,
    Monad
)


@instance(Semigroup, Result)
class ResultSemigroup:

    def combine(self, other):
        return self + other


@instance(Functor, Result)
class ResultFunctor:

    def map(self, func):
        return self.match(
            ok=lambda x: Ok(func(x)),
            err=self
        )


@instance(Applicative, Result)
class ResultApplicative:

    def ap(self, obj):
        return self.match(
            ok=lambda func: obj.match(
                ok=lambda value: Ok(func(value)),
                err=obj
            ),
            err=self
        )

    @classmethod
    def pure(cls, obj):
        return Ok(obj)


@instance(Monad, Result)
class ResultMonad:

    def flatten(self):
        return self.match(
            ok=lambda inner: inner.match(
                ok=lambda x: Ok(x),
                err=lambda e: Err(e)
            ),
            err=self
        )
