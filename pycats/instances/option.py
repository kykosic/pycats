"""
    Type class instances for Option type.
"""
from pycats import (
    Option,
    Some,
    Nil,
    instance,
    Semigroup,
    Monoid,
    Functor,
    Applicative,
    Monad
)


@instance(Semigroup, Option)
class OptionSemigroup:

    def combine(self, other):
        return self + other


@instance(Monoid, Option)
class OptionMonoid:

    @classmethod
    def unit(cls):
        return Nil()


@instance(Functor, Option)
class OptionFunctor:

    def map(self, func):
        return self.match(
            some=lambda x: Some(func(x)),
            nil=self
        )


@instance(Applicative, Option)
class OptionApplicative:

    def ap(self, obj):
        return self.match(
            some=lambda func: obj.match(
                some=lambda value: Some(func(value)),
                nil=obj
            ),
            nil=self
        )

    @classmethod
    def pure(cls, obj):
        return Some(obj)


@instance(Monad, Option)
class OptionMonad:

    def flatten(self):
        return self.match(
            some=lambda inner: inner.match(
                some=lambda x: Some(x),
                nil=inner
            ),
            nil=self
        )
