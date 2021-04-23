import pprint

from libgen_api import LibgenSearch
from requests import get

from urllib.parse import quote
from .Models import Book, LibgenResult
from .strings_ import *
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger(__name__)


def search_book(metadata: Book):
    lib_search = LibgenSearch()

    if metadata.Author:
        # filters =  {"Author": metadata.Author, "Extension": "pdf"}
        filters = {'Pages':metadata.Pages,"Extension": "pdf",'Language': 'English'}

        results = lib_search.search_title_filtered(
            f'{metadata.Title}', filters, exact_match=False
        )
    else:
        results = lib_search.search_title(metadata.Title)
    pprint.pprint(results)
    books = list(map(LibgenResult, results))

    return books


def openlibrary_lookup(book: Book):

    base_url = books_api_call.format(quote(book.Title))
    results = get(base_url).json()["items"]

    books = []

    for result in results:
        _id = result["id"]

        volume = result["volumeInfo"]
        try:
            volume['pageCount']
        except:
            continue
        if not "imageLinks" in volume or not "authors" in volume:
            continue
        try:
            subtitle = volume["subtitle"]
        except:
            subtitle = ""
            pass

        try:
            isbn = volume["industryIdentifiers"][0]["identifier"]
        except:
            isbn = ""

        book = Book(
            id=_id,
            Title=volume["title"],
            subtitle=subtitle,
            Author=",".join(volume["authors"]),
            Cover=books_api_image.format(_id),
            Year=None,
            Isbn=isbn,
            Pages=str(volume['pageCount'])
        )

        books.append(book)

    return books
