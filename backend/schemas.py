from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool

    class Config:
        orm_mode = True

class BorrowedBookBase(BaseModel):
    book_id: int
    borrow_date: date
    due_date: date

class BorrowedBookCreate(BorrowedBookBase):
    pass

class BorrowedBook(BorrowedBookBase):
    id: int
    user_id: int
    return_date: Optional[date] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
