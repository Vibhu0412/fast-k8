from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    author_id: int
    