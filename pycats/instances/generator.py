"""
    Type class instances for Python generators.
"""
from pycats import (
    generator,
    instance,
    Semigroup,
    Monoid,
    Functor,
    Applicative,
    Monad,
    Pipe
)


@instance(Semigroup, generator)
class GeneratorSemigroup:

    def combine(self, other):
        for x in self:
            yield x
        for y in other:
            yield y


@instance(Monoid, generator)
class GeneratorMonoid:

    @classmethod
    def unit(cls):
        return (_ for _ in range(0))


@instance(Functor, generator)
class GeneratorFunctor:

    def map(self, func):
        return (func(x) for x in self)


@instance(Applicative, generator)
class GeneratorApplicative:

    def ap(self, obj):
        len_err = (
            "The function generator must have the "
            "same length as object generator"
        )

        for func in self:
            try:
                value = next(obj)
            except StopIteration:
                raise TypeError(len_err)

            yield func(value)

        try:
            next(obj)
        except StopIteration:
            pass
        else:
            raise TypeError(len_err)

    @classmethod
    def pure(cls, obj):
        yield obj


@instance(Monad, generator)
class GeneratorMonad:

    def flatten(self):
        return (x for ls in self for x in ls)


@instance(Pipe, generator)
class GeneratorPipe:

    def pipe(self, func):
        return func(self)
