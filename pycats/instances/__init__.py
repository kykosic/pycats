# flake8: noqa
from .bool import (
    BoolSemigroup,
    BoolMonoid
)
from .float import (
    FloatSemigroup,
    FloatMonoid
)
from .generator import (
    GeneratorSemigroup,
    GeneratorMonoid,
    GeneratorFunctor,
    GeneratorApplicative,
    GeneratorMonad,
    GeneratorPipe
)
from .int import (
    IntSemigroup,
    IntMonoid
)
from .list import (
    ListSemigroup,
    ListMonoid,
    ListFunctor,
    ListApplicative,
    ListMonad
)
from .option import (
    OptionSemigroup,
    OptionMonoid,
    OptionFunctor,
    OptionApplicative,
    OptionMonad
)
from .result import (
    ResultSemigroup,
    ResultFunctor,
    ResultApplicative,
    ResultMonad
)
from .set import (
    SetSemigroup,
    SetMonoid,
    SetFunctor
)
from .str import (
    StrSemigroup,
    StrMonoid
)
from .tuple import (
    TupleSemigroup,
    TupleMonoid,
    TupleFunctor,
    TupleApplicative,
    TupleMonad
)
