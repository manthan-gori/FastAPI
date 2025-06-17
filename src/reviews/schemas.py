from src.shared.schemas import ReviewModel

from pydantic import BaseModel
import uuid

class ReviewCreateModel(BaseModel):
    rating: int
    review_text: str
    book_uid: uuid.UUID
# ...other review schemas...


# from pydantic import BaseModel
# from datetime import datetime
# from typing import TYPE_CHECKING
# import uuid

# if TYPE_CHECKING:
#     from src.books.schemas import Book

# class ReviewModel(BaseModel):
#     uid: uuid.UUID
#     user_uid: uuid.UUID
#     book_uid: uuid.UUID
#     rating: int
#     review_text: str
#     created_at: datetime
#     updated_at: datetime

# Example if you want to reference Book in a review detail model:
# class ReviewDetailModel(BaseModel):
#     book: "Book"
# ReviewDetailModel.model_rebuild()