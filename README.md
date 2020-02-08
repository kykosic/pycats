# PyCats
Functional Python with Typeclasses and Categories

__Disclaimer:__ This library is intended for fun/educational use only. The patterns implemented here strongly contradict all common Python best practices. If you are truly interested in functional programming and category theory, I recommend trying a more appropriate language such as Scala or Haskell.

### Contents
* [Overview](#overview)
* [Typeclass Syntax](#typeclass-syntax)
* [Typeclass Instances](#typeclass-instances)
* [Data Types](#data-types)
* [Development](#development)

<a name="overview"></a>
##  Overview

PyCats provides syntax to implement Typeclasses and some basic functional abstractions in Python. The name comes from the [Scala library: Cats](https://github.com/typelevel/cats), which get its name from the mathematical field [Cateogry theory](https://en.wikipedia.org/wiki/Category_theory).

Unlike true functional ecosystems, Python is dynamically typed. While this makes it easy to implement things quickly, it makes code prone to errors at runtime. Python 3 does support type annotations and has static analysis tools such as `mypy` to detect errors in code. However, it does not support higher-kinded type generics, making it impossible to annotate this library. As a result, all code here is dynamically typed and correct use is left to the user.

Installation (from source):
```
git clone https://github.com/kykosic/pycats.git
cd pycats
pip install .
```

<a name="typeclass-syntax"></a>
## Typeclass Syntax
At the core of this library is the ability to declare typeclasses and instances on any object. This is also the part that strongly disagrees with Python best practices. To declare a typeclass:
```python
>>> from abc import ABC, abstractmethod
>>> from pycats import typeclass, instance
>>>
>>> @typeclass
... class Functor(ABC):
...
...     @abstractmethod
...     def map(self, func):
...         pass
>>>
```
A typeclass cannot be directly instantiated. Instead, instances of typeclasses are implemented for different objects. To implement the `Functor` typeclass for `list` objects:
```python
>>> @instance(Functor, list)
... class ListFunctor:
...
...     def map(self, func):
...         return [func(x) for x in self]
>>>
```
Now as long as the `ListFunctor` instance is in scope, we can use the `.map` method on lists:
```python
>>> [1, 2, 3].map(lambda x: x + 1)
[2, 3, 4]
```

Note that typeclasses use the abstract base class (ABC) with abstractmethod decorators denoting which methods should be implemented by instances. Typeclasses are allowed to implement non-abstract methods, which will also be given to objects through the instance.

<a name="typeclasses-instances"></a>
## Typeclass Instances
A small set of common typeclasses from category theory have been included in this library (with more to come later). This currently includes:
* Semigroup
    * `.combine`
* Monoid
    * `.unit`
* Functor
    * `.map`
* Applicative
    * `.ap`
    * `.pure`
* Monad
    * `.flatten`
    * `.flat_map`
* Pipe
    * `.pipe`

Instances for these type classes are provided for the following objects (when applicable):
* bool
* float
* generator
* int
* list
* Option
* Result
* set
* str
* tuple

To import all typeclass instances, simply import the `pytest.instances` module. For example, you can access the `Monad` instance for a `list` as follows:
```python
>>> import pycats.instances
>>>
>>> [1, 2, 3].flat_map(lambda x: list(range(x)))
[0, 0, 1, 0, 1, 2]
```


<a name="data-types"></a>
## Data Types
PyCats includes a number of additional data types (type constructors) to fill in some of the functional gaps of the standard library. These can be found in `pycats.data`.

### Option
The `Option[A]` data type is a type constructor inspired by Scala's option type, having sub-types `Some[A]` and `Nil`. It represents an object containing a value with generic type `A` or is null. Options come equipped with a `.match` method to pattern-match on "some" and "nil" with syntax similar to Scala or Rust. Some example uses:
```python
>>> from pycats import Option, Some, Nil
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
>>> 
>>> print(a.unwrap())
1
>>> print(b.unwrap())
None
>>> 
>>> Some(2) + Some(3)
Some(5)
>>> Some(1) + Nil()
Nil()
```

### Result
The `Result[A, E]` data type is a type constructor inspired by Rust's result type, having sub-types `Ok[A]` and `Err[E]`. It represents an object containing a value of generic type `A` or an error object containing exception of generic type `E`. It also has a `.match` function to pattern-match on "ok" and "err" with syntax similar to Rust. Some example uses:
```python
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
>>> 
>>> b.match(
...     ok=lambda x: f'Success! Result is: {x}',
...     err=lambda x: f'Failed! Error: {x}'
... )
'Failed! Error: Bad value!'
>>> 
>>> a.unwrap()
1
>>> b.unwrap()
Traceback (most recent call last):
  File "pycats/pycats/data/result.py", line 77, in unwrap
    raise self.value
ValueError: Bad value!
```
Additionally, the `Result` class has a decorator to wrap any function. This will automatically warp the output in an `Ok` object and catch any exceptions in an `Err` object.
```python
>>> @Result.wrap
... def divide(a, b):
...     return a / b
...
>>> divide(6, 3)
Ok(2.0)
>>> divide(2, 0)
Err(division by zero)
``` 
This allows programs to propogate errors more gracefully than having arbitrarily nested exception catching. For example:
```python
>>> def print_result(res: Result):
...     text = res.match(
...         ok=lambda x: f'Success: {x}',
...         err=lambda x: f'Error: {x}'
...     )
...     print(text)
...
>>> print_result(divide(6, 4))
Success: 1.5
>>> print_result(divide(2, 0))
Error: division by zero
```

### Generators
This library exposes the Python buildin `generator` object in `pycats.generator` so that typclass instances can be created for it. This allows for a functional interface to interact with lazy "streaming" data.

For examples of how typeclasses can be used on streams, see [the lazy generator example](examples/lazy_generators.py).

<a name="development"></a>
##  Development
This library is compatible with Python 3.6+. To install in editable mode with development dependencies:
```
pip install -e ".[dev]"
``` 
#### Unit tests
Tests are located in the `pycats/tests` folder and are structured to mirror the rest of the repo. After the above install is done, unit tests can be run with:
```
pytest --doctest-modules
```

#### Linting
Similar to unit tests, linting can be run from the root directory with:
```
flake8
```
