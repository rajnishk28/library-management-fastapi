from typing import Optional
from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    category: str
    quantity: int
    available: int


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    available: Optional[int] = None
