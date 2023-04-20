from functools import reduce
from typing import TypeVar, Callable, Sequence

T = TypeVar("T")


def pipeline(
    value: T,
    functions: Sequence[Callable[[T], T]],
) -> T:
    return reduce(lambda v, f: f(v), functions, value)
