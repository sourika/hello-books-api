from flask import Blueprint
from app.models.book import books

book_bp = Blueprint("book", __name__, url_prefix="/books")

@book_bp.get("")
def get_all_books():
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
