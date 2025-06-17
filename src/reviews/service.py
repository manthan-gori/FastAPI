from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
import logging
from src.errors import BookNotFound, UserNotFound

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(
            self,
            user_email: str, 
            book_uid: str, 
            review_data: ReviewCreateModel, 
            session: AsyncSession
    ):
        try:
            book = await book_service.get_book(
                book_uid=book_uid,
                session=session
            )

            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )
            review_data_dict = review_data.model_dump()
            new_review = Reviews(**review_data_dict)

            if not book:
                raise BookNotFound()
            if not user:
                raise UserNotFound()
            new_review.user_uid = user.user_id 
            new_review.book_uid = book.uid
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong.")










# from fastapi.exceptions import HTTPException
# from fastapi import status
# from sqlmodel.ext.asyncio.session import AsyncSession
# from src.db.models import Reviews
# from src.auth.service import UserService
# from src.books.service import BookService
# from .schemas import ReviewCreateModel
# import logging


# book_service = BookService()
# user_service = UserService()


# class ReviewService:
#     async def add_review_to_book(
#             self,
#             user_email: str, 
#             book_uid: str, 
#             review_data: ReviewCreateModel, 
#             session: AsyncSession
#     ):
#         try:
#             books = await book_service.get_books(
#                 book_uid=book_uid,
#                 session=session
#             )
#             user = await user_service.get_user_by_email(
#                 email=user_email,
#                 session=session
#             )
#             review_data_dict = review_data.model_dump()
#             new_review = Reviews(**review_data_dict)

#             if not book:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
#             if not user:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            

#             new_review.user_uid = user.user_id 
#             new_review.book_uid = books.uid
#             session.add(new_review)
#             await session.commit()
#             return new_review

#         except Exception as e:
#             logging.exception(e)
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Oops something went wrong.")