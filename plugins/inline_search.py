from pyrogram.types import *
from pyrogram import Client
from utils.Models import *
from utils.Scaper import openlibrary_lookup
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger(__name__)


@Client.on_inline_query()
async def inline_callback(client: Client, inline_query: InlineQuery):
    search_term = inline_query.query
    inline_results = []
    if search_term:
        results = openlibrary_lookup(Book(Title=search_term))
        books = map(SearchResult, results)
        inline_results = [i.article for i in books]
        inline_results = inline_results[:50]
    await inline_query.answer(results=inline_results)


@Client.on_chosen_inline_result()
async def process_chosen_result(client: Client, choice: ChosenInlineResult):
    message_id = choice.inline_message_id
    chat_id = choice.from_user.id


@Client.on_callback_query()
async def handle_callback(client: Client, callback_query: CallbackQuery):
    result:Library=session.query(Library).filter_by(id=callback_query.data).first()
    await callback_query.edit_message_text(text=result.Title)

