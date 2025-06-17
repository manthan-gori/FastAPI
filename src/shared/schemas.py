from pydantic import BaseModel
from datetime import datetime
import uuid

class ReviewModel(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    rating: int
    review_text: str
    created_at: datetime
    updated_at: datetime