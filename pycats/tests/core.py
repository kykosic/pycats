from abc import ABC, abstractmethod

import pytest

from pycats import typeclass, instance


def test_typeclass():

    @typeclass
    class Foo(ABC):

        @abstractmethod
        def foo_fn(self):
            pass

    with pytest.raises(TypeError, match="typeclass"):
        Foo()

    with pytest.raises(TypeError, match="should inherit"):

        @typeclass
        class Foo:

            @abstractmethod
            def foo_fn(self):
                pass


def test_instance():

    @typeclass
    class Foo(ABC):

        @abstractmethod
        def foo_fn(self):
            pass

    @typeclass
    class Bar(Foo, ABC):

        @abstractmethod
        def bar_fn(self):
            pass

        def give_one(self):
            return 1

    @instance(Foo, int)
    class IntFoo:

        def foo_fn(self):
            return self + 1

    @instance(Bar, int)
    class IntBar:

        def bar_fn(self):
            return self * 2

    actual = (1).foo_fn()
    expected = 2
    assert actual == expected

    actual = (2).bar_fn()
    expected = 4
    assert actual == expected

    actual = (3).give_one()
    expected = 1
    assert actual == expected

    with pytest.raises(TypeError, match="typeclass instance"):
        IntBar()

    with pytest.raises(TypeError, match="missing implementations"):
        @instance(Foo, str)
        class StrFoo:
            pass

    class Obj:

        def __init__(self, value):
            self.value = value

    @instance(Foo, Obj)
    class ObjFoo:

        def foo_fn(self):
            return self.value + 4

    actual = Obj(3).foo_fn()
    expected = 7
    assert actual == expected
