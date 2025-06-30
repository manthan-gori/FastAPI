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
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    user_id: uuid.UUID
    email: str
    username: str
    firstname: str
    lastname: str

class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]

class EmailModel(BaseModel):
    addresses: List[str]

class PasswordResetRequestModel(BaseModel):
    email: str

class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str