from . import schemas, security

def get_user_by_email(db, email: str):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

def create_user(db, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    cursor = db.cursor()
    query = "INSERT INTO users (name, email, hashed_password, role) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user.name, user.email, hashed_password, user.role))
    db.commit()
    user_id = cursor.lastrowid
    return {"id": user_id, **user.dict()}

def get_books(db, skip: int = 0, limit: int = 10):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM books LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, skip))
    return cursor.fetchall()

def get_book_by_title_and_author(db, title: str, author: str):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM books WHERE title = %s AND author = %s"
    cursor.execute(query, (title, author))
    return cursor.fetchone()

def create_book(db, book: schemas.BookCreate):
    cursor = db.cursor()
    query = "INSERT INTO books (title, author, genre, available) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (book.title, book.author, book.genre, book.available))
    db.commit()
    book_id = cursor.lastrowid
    return {"id": book_id, **book.dict()}

def borrow_book(db, user_id: int, book_id: int, borrow_date: str, due_date: str):
    cursor = db.cursor()
    query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, book_id, borrow_date, due_date))
    borrow_id = cursor.lastrowid

    update_query = "UPDATE books SET available = False WHERE id = %s"
    cursor.execute(update_query, (book_id,))

    db.commit()
    return {"id": borrow_id, "user_id": user_id, "book_id": book_id, "borrow_date": borrow_date, "due_date": due_date}

def return_book(db, borrow_id: int, return_date: str):
    cursor = db.cursor(dictionary=True)

    update_borrow_query = "UPDATE borrowed_books SET return_date = %s WHERE id = %s"
    cursor.execute(update_borrow_query, (return_date, borrow_id))

    select_book_query = "SELECT book_id FROM borrowed_books WHERE id = %s"
    cursor.execute(select_book_query, (borrow_id,))
    result = cursor.fetchone()
    book_id = result['book_id']

    update_book_query = "UPDATE books SET available = True WHERE id = %s"
    cursor.execute(update_book_query, (book_id,))

    db.commit()

    select_borrowed_book_query = "SELECT * FROM borrowed_books WHERE id = %s"
    cursor.execute(select_borrowed_book_query, (borrow_id,))
    return cursor.fetchone()
