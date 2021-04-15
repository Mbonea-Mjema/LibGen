from libgen_api import LibgenSearch
from requests import get
from urllib.parse import quote
from .Models import Book,LibgenResult
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)



def search_book(metadata:Book):
    lib_search = LibgenSearch()

    if metadata.Author:
        filters = {"Author": metadata.Author, "Extension": "pdf"}
        results=lib_search.search_title_filtered(metadata.Title, filters, exact_match=False)
    else:
        results=lib_search.search_title(metadata.Title)
    books =map(LibgenResult,results)
    return books


def openlibrary_lookup(book:Book):

    base_url = f"https://www.googleapis.com/books/v1/volumes?q={quote(book.Title)}&key=AIzaSyBbphNVAq9wGTsSMQAqRmmKxvTgjllrQNA"
    results =get(base_url).json()['items']

    books =[]

    for result in results:
        _id =result['id']

        volume = result['volumeInfo']
        if not 'imageLinks' in volume or  not 'authors' in volume:
            continue
        try:
            subtitle = volume['subtitle']
        except:
            subtitle = None
            pass

        try:
            desccription = volume['description']
        except:
            desccription = None
            pass
        book=Book(id=_id,Title=volume['title'],subtitle=subtitle,Author=','.join(volume['authors']),Cover=volume['imageLinks']['thumbnail'],Year=None,description=desccription)
        books.append(book)


    return books






