from pyrogram.types import *
from pyrogram import Client
from utils.Models import SearchResult,Book
from utils.Scaper import openlibrary_lookup
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)

@Client.on_inline_query()
async def inline_callback(client: Client, inline_query: InlineQuery):
    search_term = inline_query.query
    inline_results=[]
    if search_term:
        results=openlibrary_lookup(Book(Title=search_term))
        books = map(SearchResult,results)
        inline_results=[i.article  for i in books]
        inline_results =inline_results[:50]
    await  inline_query.answer(results=inline_results)
