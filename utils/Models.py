from dataclasses import dataclass, asdict
from pyrogram.types import *
from .DbModels import *
from uuid import uuid4
from urllib.parse import quote
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger(__name__)


@dataclass
class Book:
    id: str = ""
    title: str = ""
    subtitle: str = ""
    Author: str = ""
    Cover: str = ""
    Year: str = ""
    Isbn: str = ""
    Pages: str = ""
    Publisher: str = ""
    Categories: str = ""


class LibgenResult(Book):
    def __init__(self, result: dict):
        self.title = result["Title"]
        self.Author = result["Author"]
        self.Language = result["Language"]
        self.Year = result["Year"]
        self.Size = result["Size"]
        self.Type = result["Extension"]
        self.Link = result["Mirror_1"]
        self.Pages = result["Pages"]
        self.Publisher = result["Publisher"]


def message_gen(book: Book):
    caption = ""
    caption += f"📚 **title:{book.title}**\n\n"
    caption += f"🧐 **Author:{book.Author}**\n"
    if book.Year:
        caption += f"📅**Year={book.Year}**\n"
    if book.Isbn:
        caption += f"🆔**Isbn:{book.Isbn}**\n"
    return caption


class SearchResult:
    def __init__(self, book: Book):
        self.title = f"{book.title}: {book.subtitle}"
        self.thumb = book.Cover
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(callback_data=book.id, text="Download ⬇")]]
        )

        self.article = InlineQueryResultPhoto(
            photo_url=self.thumb,
            title=book.title,
            caption=message_gen(book),
            reply_markup=reply_markup,
        )

        result = session.query(Library).filter_by(id=book.id).first()
        if result:
            pass
        else:
            f = Library(book)
            session.add(f)
            session.commit()
