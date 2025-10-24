from flask import Blueprint, abort, make_response, request
from app.models.book import Book
from ..db import db
# from app.models.book import books

books_bp = Blueprint("book", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201


@books_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response

# @book_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response


# @book_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)
#     return {
#             "id": book.id,
#             "title": book.title,
#             "description": book.description,
#         }


# def validate_book(book_id):
#     try:
#        book_id = int(book_id)
#     except ValueError:
#         response = {"message": f"Book id {book_id} invalid"}
#         return abort(make_response(response, 400)) 
    
#     for book in books:
#         if book.id == book_id:
#             return book
#     response = {"message": f"Book id {book_id} not found"}
#     return abort(make_response(response, 404))   
