from fastapi import APIRouter , Depends
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from .service import ReviewService

review_service = ReviewService()

review_router = APIRouter()

@review_router.post('/book/{book__uid}')
async def add_review_to_books(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        current_user.email,
        book_uid,
        review_data,
        session = session
    )
    return new_review