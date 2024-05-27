from __future__ import annotations
import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar
T = TypeVar("T")
__all__ = ["run_with_asyncio"]
def run_with_asyncio(f: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        print("pajinlail")
        return asyncio.run(f(*args, **kwargs))
    return wrapper