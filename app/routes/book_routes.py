from flask import Blueprint, Response, abort, make_response, request
from app.models.book import Book
from app.models.author import Author
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("book", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    try:
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    db.session.add(new_book)
    db.session.commit()
    return new_book.to_dict(), 201


@bp.get("")
def get_all_books():
    query = db.select(Book)
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Book.id)
    books = db.session.scalars(query)
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return books_response # [b.to_dict() for b in books]

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
