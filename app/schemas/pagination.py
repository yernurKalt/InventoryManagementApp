from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class PageMeta(BaseModel):
    limit: int
    offset: int
    total: int


class Page(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta