from pydantic import BaseModel, Field
from typing import List
from src.books.schemas import Book
from src.shared.schemas import ReviewModel
import uuid

class UserCreateModel(BaseModel):
    email: str
    password: str
    username: str
    firstname: str
    lastname: str

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(max_length=20)

class UserModel(BaseModel):
    user_id: uuid.UUID
    email: str
    username: str
    firstname: str
    lastname: str

class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]