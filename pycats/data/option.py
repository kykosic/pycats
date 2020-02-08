"""
    Option data type, with behavior similar Scala's Option type.
"""
from abc import ABC, abstractmethod


class Option(ABC):
    """ A type constructor containing either a value, or nothing.

    Given generic type `A`, an `Option[A]` can either be `Some[A]` or `Nil`.

    Examples:
        >>> from pycats import Option, Some, Nil
        >>>
        >>> Some(1)
        Some(1)
        >>> Nil()
        Nil()
        >>> Some(2) + Some(3)
        Some(5)
        >>> Some(1) + Nil()
        Nil()
        >>> Some('cat') == Some('cat')
        True
        >>> Some('cat') == Some('dog')
        False
        >>> if Some(1):
        ...     print("Has a value!")
        ...
        Has a value!
        >>> if Nil():
        ...     print("Has a value!")
        ...
        >>>
        >>> print(Some(1).unwrap())
        1
        >>> print(Nil().unwrap())
        None
    """

    def match(self, some, nil):
        """ Pattern match on the two cases for options.

        Examples:
            >>> from pycats import Some, Nil
            >>>
            >>> a = Some(1)
            >>> b = Nil()
            >>>
            >>> a.match(
            ...     some=lambda x: f'I have some value: {x}',
            ...     nil='I have no value'
            ... )
            'I have some value: 1'
            >>>
            >>> b.match(
            ...     some=lambda x: f'I have some value: {x}',
            ...     nil='I have no value'
            ... )
            'I have no value'

        Args:
            some: The value to return or function to call if this object is
                a `Some[A]`. Function should have signature `A -> Any`.
            nil: The value to return or function to call if this object is
                a `Nil`. Function should have signature `() -> Any`.

        Returns:
            Value or result of function for the appropriate type.

        """
        if isinstance(self, Some):
            if callable(some):
                return some(self.value)
            return some
        elif isinstance(self, Nil):
            if callable(nil):
                return nil()
            return nil
        raise TypeError(
            f"Expected Option, got {self.__class__.__name__})")

    def __add__(self, other):
        return self.match(
            some=lambda x: other.match(
                some=lambda y: Some(x + y),
                nil=Nil()
            ),
            nil=Nil()
        )

    def __bool__(self):
        return self.match(
            some=True,
            nil=False
        )

    def __eq__(self, other):
        return self.match(
            some=lambda x: other.match(
                some=lambda y: x == y,
                nil=False
            ),
            nil=lambda: other.match(
                some=False,
                nil=True
            )
        )

    @abstractmethod
    def unwrap(self):
        """ Return the inner value for `Some[A]` or `None` for `Nil`.

            The `.match` method should be preferred.
        """
        pass


class Some(Option):
    """ `Some[A]` variation of `Option[A]`. """

    def __init__(self, value):
        self.value = value

    def unwrap(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class Nil(Option):
    """ `Nil` variation of `Option[A]`. """

    def unwrap(self):
        return None

    def __repr__(self):
        return f"{self.__class__.__name__}()"
