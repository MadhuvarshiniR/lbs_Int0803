from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from . import crud, schemas, security, dependencies
from .config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, date

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(dependencies.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_user)):
    return current_user

@router.post("/books/", response_model=schemas.Book, dependencies=[Depends(dependencies.get_current_librarian)])
def create_book(book: schemas.BookCreate, db = Depends(dependencies.get_db)):
    db_book = crud.get_book_by_title_and_author(db, title=book.title, author=book.author)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db=db, book=book)

@router.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db = Depends(dependencies.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.post("/borrow/", response_model=schemas.BorrowedBook)
def borrow_book(borrow: schemas.BorrowedBookCreate, db = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_current_user)):
    # This is a placeholder for the logic to check if a book is available
    # In a real application, you would query the database for the book
    # and check its availability.
    # For now, we'll assume the book is available.
    today = date.today()
    due_date = today + timedelta(days=14)

    return crud.borrow_book(db=db, user_id=current_user['id'], book_id=borrow.book_id, borrow_date=today, due_date=due_date)

@router.post("/return/{borrow_id}", response_model=schemas.BorrowedBook)
def return_book(borrow_id: int, db = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_current_user)):
    # This is a placeholder for the logic to check the borrow record
    # In a real application, you would query the database for the record
    # and check its status.
    # For now, we'll assume the record is valid.
    return_date = date.today()
    return crud.return_book(db=db, borrow_id=borrow_id, return_date=return_date)
