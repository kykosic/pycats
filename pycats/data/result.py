"""
    Result data type, with behavior similar to Rust's Result type.
"""
import functools
from abc import ABC, abstractmethod


class Result(ABC):
    """ A type constructor containing either a value or an exception.

    Given generic type `A` and error type `E`, a `Result[A, E]` can
        either be `Ok[A]` or `Err[E]`.

    Examples:
        >>> from pycats import Result, Ok, Err
        >>>
        >>> Ok(1)
        Ok(1)
        >>> Err(ValueError('Bad value!'))
        Err(Bad value!)
        >>> Ok(3) + Ok(4)
        Ok(7)
        >>> Ok(3) + Err(ValueError('Bad value!'))
        Err(Bad value!)
        >>> Ok('cat') == Ok('cat')
        True
        >>> Ok('cat') == Ok('dog')
        False
        >>>
        >>> a = Ok(1)
        >>> b = Err(ValueError('Bad value!'))
        >>> a.unwrap()
        1
        >>> b.unwrap()
        Traceback (most recent call last):
          File "pycats/data/result.py", line 86, in unwrap
            raise self.value
        ValueError: Bad value!

    """

    def __init__(self, value):
        self.value = value

    def match(self, ok, err):
        """ Pattern match on the two cases for results.

        Examples:
            >>> from pycats import Result, Ok, Err
            >>>
            >>> a = Ok(1)
            >>> b = Err(ValueError('Bad value!'))
            >>>
            >>> a.match(
            ...     ok=lambda x: f'Success! Result is: {x}',
            ...     err=lambda x: f'Failed! Error: {x}'
            ... )
            'Success! Result is: 1'
            >>> b.match(
            ...     ok=lambda x: f'Success! Result is: {x}',
            ...     err=lambda x: f'Failed! Error: {x}'
            ... )
            'Failed! Error: Bad value!'

        Args:
            ok: The value to return or function to call if this object is
                a `Ok[A]`. Function should have signature `A -> Any`.
            err: The value to return or function to call if this object is
                an `Err[E]`. Function should have signature `E -> Any`.

        Returns:
            Value or result of function for the appropriate type.
        """
        if isinstance(self, Ok):
            if callable(ok):
                return ok(self.value)
            return ok
        elif isinstance(self, Err):
            if callable(err):
                return err(self.value)
            return err
        raise TypeError(
            f"Expected Result instance, got {self.__class__.__name__})")

    @staticmethod
    def wrap(func):
        """ Decorator to automatically wrap the result of a function call.

        Examples:
            >>> from pycats import Result
            >>>
            >>> @Result.wrap
            ... def divide(a, b):
            ...     return a / b
            ...
            >>> divide(6, 3)
            Ok(2.0)
            >>> divide(2, 0)
            Err(division by zero)

        Args:
            func: The function to wrap and catch exceptions.

        Returns:
            Wrapped function that is exception-safe. If `func` had signature
                of `A -> B`, then the wrapped function is `A -> Result[B, E]`

        """
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            try:
                return Ok(func(*args, **kwargs))
            except Exception as e:
                return Err(e)
        return wrapped_func

    def __add__(self, other):
        return self.match(
            ok=lambda x: other.match(
                ok=lambda y: Ok(x + y),
                err=other
            ),
            err=self
        )

    def __bool__(self):
        return self.match(
            ok=True,
            err=False
        )

    def __eq__(self, other):
        return self.match(
            ok=lambda x: other.match(
                ok=lambda y: x == y,
                err=False
            ),
            err=False
        )

    @abstractmethod
    def unwrap(self):
        """ Return the inner value for `Ok[A]` or raise `E` for `Err[E]`.

            The `.match` method should be preferred.
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class Ok(Result):
    """ The `Ok[A]` variation of `Result[A, E]`. """

    def unwrap(self):
        return self.value


class Err(Result):
    """ The `Err[E]` variation of `Result[A, E]`. """

    def unwrap(self):
        if isinstance(self.value, Exception):
            raise self.value
        return self.value
