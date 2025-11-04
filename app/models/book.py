from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author
class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id")) 
    author: Mapped[Optional["Author"]] = relationship(back_populates="books") 


    def to_dict(self):
        book_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }

        if self.author:
            book_as_dict["author"] = self.author.name
            book_as_dict["author_id"] = self.author.id
        return book_as_dict
    

    @classmethod
    def from_dict(cls, book_data):
        book = cls(title=book_data["title"],
                description=book_data["description"])
        if "author_id" in book_data:
            book.author_id = book_data["author_id"]
        return book    