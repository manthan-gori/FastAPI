from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.db.main import get_session
from .schemas import Book, BookUpdateModel, BookCreateModel, BookDetailModel
from src.auth.dependencies import AccessTokenBearer , RoleChecker
from src.errors import BookNotFound

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))

@book_router.get("/", response_model=List[Book] , dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ):
    print("session=",session)
    books = await book_service.get_all_books(session)
    return books



@book_router.get("/user/{userr_uid}", response_model=List[Book] , dependencies=[role_checker])
async def get_user_book_submissions(
    user_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ):
    print("session=",session)
    books = await book_service.get_user_books(user_uid , session)
    return books




@book_router.post(
        "/",
        status_code=status.HTTP_201_CREATED, 
        response_model=Book, 
        dependencies=[role_checker]
        )
async def create_a_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) -> dict:
    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid, session)
    return new_book

@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_uid: str, session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise BookNotFound()

@book_router.patch(
        "/{book_uid}", 
        response_model=Book, 
        dependencies=[role_checker])
async def update_book(
    book_uid: str, 
    book_update_data: BookUpdateModel, 
    session: AsyncSession = Depends(get_session), 
    token_details : dict = Depends(access_token_bearer)
    ) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise BookNotFound()

@book_router.delete(
        "/{book_uid}", 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[role_checker])
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ):
    book_deleted = await book_service.delete_book(book_uid, session)
    if book_deleted:
        return None
    else:
        raise BookNotFound()