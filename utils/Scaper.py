import pprint

from libgen_api import LibgenSearch
from requests import get
from fuzzywuzzy import fuzz
from urllib.parse import quote
from .Models import Book, LibgenResult
from .strings_ import *
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger(__name__)


def find_best_match(book: Book, results):
    scores = []
    print(book)
    type_filter = "pdf,epub"
    if "Computer" in book.Categories:
        type_filter = "pdf"
    for result in results:
        temp = 1.0
        temp_scores = []
        if not result["Extension"] in type_filter:
            scores.append(0)
            continue

        temp_scores.append(fuzz.ratio(book.Author, result["Author"]) / 100)
        temp_scores.append(fuzz.ratio(book.Title, result["Title"]) / 100)
        temp_scores.append(0.5 * fuzz.ratio(book.Pages, result["Pages"]) / 100)
        print("publisher=", book.Publisher, result["Publisher"])
        temp_scores.append(0.8 * fuzz.ratio(book.Publisher, result["Publisher"]) / 100)
        temp = 0
        for score in temp_scores:
            if score == 0:
                continue
            temp += score
        scores.append(temp)
    pprint.pprint(scores)
    if scores:
        best_score = max(scores)
        if best_score > 1.9:
            print(best_score)
            return scores.index(best_score)


def search_book(metadata: Book):
    lib_search = LibgenSearch()

    if metadata.Author:
        # filters =  {"Author": metadata.Author, "}
        filters = {"Language": "English"}

        results = lib_search.search_title_filtered(
            f"{metadata.Title}", filters, exact_match=False
        )
    else:
        results = lib_search.search_title(metadata.Title)
    pprint.pprint(results)
    best = find_best_match(metadata, results)
    if best != None:
        best = results[best]

        best = LibgenResult(best)
        print(best)
        return best


def openlibrary_lookup(book: Book):

    base_url = books_api_call.format(quote(book.Title))
    results = get(base_url).json()["items"]

    books = []

    for result in results:
        _id = result["id"]

        volume = result["volumeInfo"]
        try:
            volume["pageCount"]
        except:
            continue
        try:
            categories = volume["categories"][0]
        except:
            categories = ""
        if not "imageLinks" in volume or not "authors" in volume:
            continue
        try:
            subtitle = volume["subtitle"]
        except:
            subtitle = ""
            pass
        try:
            publisher = volume["publisher"]
        except:
            continue
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
            Pages=str(volume["pageCount"]),
            Publisher=publisher,
            Categories=categories,
        )

        books.append(book)

    return books
