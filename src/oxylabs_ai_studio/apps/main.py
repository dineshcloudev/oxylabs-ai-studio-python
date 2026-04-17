from collections.abc import Callable
from typing import Any, TypeVar, cast

from fastapi import FastAPI

app = FastAPI()

_RouteFunc = TypeVar("_RouteFunc", bound=Callable[..., Any])


def _typed_get(path: str) -> Callable[[_RouteFunc], _RouteFunc]:
    return cast(Callable[[_RouteFunc], _RouteFunc], app.get(path))


@_typed_get("/")
def health() -> dict[str, str]:
    return {"status": "running"}
