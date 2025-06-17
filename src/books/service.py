from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select
from src.db.models import Book
from sqlalchemy import desc

class BookService:



    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        return result.first()




    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, userr_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == userr_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def create_book(self, book_data: BookCreateModel, userr_uid:str , session: AsyncSession):
        new_book = Book(**book_data.dict())  # Assuming `BookCreateModel` has a `dict()` method
        session.add(new_book)
        new_book.user_uid = userr_uid
        await session.commit()
        await session.refresh(new_book)  # Refresh to get the new book's data (like its generated ID)
        return new_book

    async def update_book(
            self,
            book_uid: str, 
            update_data: BookUpdateModel, 
            session: AsyncSession
            ):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is not None:
            for k, v in update_data.dict().items():
                setattr(book_to_update, k, v)
            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return False
