from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_title_and_author(db: Session, title: str, author: str):
    return db.query(models.Book).filter(models.Book.title == title, models.Book.author == author).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def borrow_book(db: Session, user_id: int, book_id: int, borrow_date: str, due_date: str):
    db_borrow = models.BorrowedBook(user_id=user_id, book_id=book_id, borrow_date=borrow_date, due_date=due_date)
    db.add(db_borrow)
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    book.available = False
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

def return_book(db: Session, borrow_id: int, return_date: str):
    borrow_record = db.query(models.BorrowedBook).filter(models.BorrowedBook.id == borrow_id).first()
    borrow_record.return_date = return_date
    book = db.query(models.Book).filter(models.Book.id == borrow_record.book_id).first()
    book.available = True
    db.commit()
    return borrow_record
