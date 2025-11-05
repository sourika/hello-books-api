from flask import Blueprint, Response, abort, make_response, request
from app.models.book import Book
from app.models.author import Author
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("book", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)


@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    if "title" in request_body:
        book.title = request_body["title"]
    if "description" in request_body:
        book.description = request_body["description"]
    if "author_id" in request_body:
        if request_body["author_id"] is None:
            book.author = None
            book.author_id = None
        else:
            author = validate_model(Author, request_body["author_id"])
            book.author = author    
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


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
