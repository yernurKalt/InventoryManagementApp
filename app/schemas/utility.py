from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class Pagination(BaseModel):
    total: int
    skip: int
    limit: int