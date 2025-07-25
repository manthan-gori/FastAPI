from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import List , Optional
import uuid
from datetime import datetime , date



class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: uuid.UUID = Field(  
        default_factory=uuid.uuid4,
        primary_key=True
    )
    username: str
    email: str = Field(index=True, unique=True)
    firstname: str
    lastname: str
    role: str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False, server_default="user"
    ))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs= {"lazy":"selectin"}
    )

    reviews: List["Reviews"] = Relationship(
        back_populates="user", sa_relationship_kwargs= {"lazy":"selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"
    




class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.user_id")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(
        back_populates="book", sa_relationship_kwargs= {"lazy":"selectin"}
    )

    def __repr__(self):
        return f"<Book (title={self.title})>"

class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating : int = Field(lt=5)
    review_text : str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.user_id")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for Book {self.book_uid} by user {self.userr_uid})>"
