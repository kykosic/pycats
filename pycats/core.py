"""
    Core functionality and typeclass implementations.
"""
import builtins
from abc import ABC

from forbiddenfruit import curse


def delay_error(message, etype=TypeError):
    """ Return a thunk which raises an error when called. """

    def dispatch_error(*_, **__):
        raise etype(message)

    return dispatch_error


def typeclass(x):
    """ Decorator for declaring a typeclass.

    Examples:
        >>> from abc import ABC, abstractmethod
        >>> from pycats import typeclass
        >>>
        >>> @typeclass
        ... class Functor(ABC):
        ...
        ...     @abstractmethod
        ...     def map(self, func):
        ...         pass
        ...
        >>>

    Args:
        x: An abstract class. Must inherit from `abc.ABC`.

    Returns:
        An abstract "typeclass" object.

    """

    x.__new__ = delay_error("Cannot instantiate a typeclass")

    if not issubclass(x, ABC):
        raise TypeError("Typeclasses should inherit from `abc.ABC`")

    return x


def instance(type_cls, cls):
    """ Decorator for creating a typeclass instance.

    Examples:
        >>> from abc import ABC, abstractmethod
        >>> from pycats import typeclass, instance
        >>>
        >>> @typeclass
        ... class Functor(ABC):
        ...
        ...     @abstractmethod
        ...     def map(self, func):
        ...         pass
        ...
        >>>
        >>> @instance(Functor, list)
        ... class ListFunctor:
        ...
        ...     def map(self, func):
        ...         return [func(x) for x in self]
        ...
        >>>
        >>> [1, 2, 3].map(lambda x: x + 1)
        [2, 3, 4]

    Args:
        type_cls: An abstract `typeclass` decorated class.
        cls: The target class for which the typeclass will be implemented.

    Returns:
        The inner decorator which does the implementation patching.

    """

    def decorate(inst_cls):
        """ Inner decorator closure. """
        # Need to use special library to monkey-patch builtins
        if type(cls).__name__ in dir(builtins):
            setter = curse
        else:
            setter = setattr

        # Patch in all public instance methods to the object
        impl = set()
        for name, trait in inst_cls.__dict__.items():
            if name.startswith("_"):
                continue
            setter(cls, name, trait)
            impl.add(name)

        # Check if missing any non-inherited abstract methods
        abs_methods = getattr(type_cls, "__abstractmethods__", set())
        missing = abs_methods.intersection(type_cls.__dict__) - impl
        if missing:
            msg = ", ".join(missing)
            raise TypeError(f"{inst_cls.__name__} missing implementations "
                            f"from typeclass {type_cls.__name__}: {msg}")

        # Patch in inherited concrete public methods
        for name, trait in type_cls.__dict__.items():
            if name.startswith("_") \
                    or (name in abs_methods) \
                    or (name in inst_cls.__dict__):
                continue
            setter(cls, name, trait)

        # Prevent instances from being instantiated
        inst_cls.__new__ = delay_error(
            "Cannot instantiate a typeclass instance")

        return inst_cls

    return decorate
