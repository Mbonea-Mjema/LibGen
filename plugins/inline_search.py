from pyrogram.types import *
from pyrogram import Client
from utils.Models import *
from utils.Scaper import *
from utils.downloader import *
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
    print('this')
    book_result:Library=session.query(Library).filter_by(id=callback_query.data).first()
    books=search_book(book_result)
    if books:
        msg =''
        for i in books:
            msg+=f'{i.Title}\n'
        print(books[0].Link)

        await callback_query.answer(text='Downloading the book')
        await callback_query.edit_message_text('Downloading the book')
        path=await download_book(books[0].Link,file_name=f'{books[0].Title}',extension=books[0].Type,id=callback_query.data)
        await client.send_photo(chat_id=-1001347315127,photo=books_api_image.format(book_result.id),caption=message_gen(book_result))
        message=await client.send_document(chat_id=-1001347315127,disable_notification=True,file_name=f'{book_result.Title}.pdf',document=path,caption='@testlib34')
        await callback_query.edit_message_text(book_result.Title,reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(url=channel_message_link.format(message.message_id),text=book_result.Title)]]
        )
                                               )
    else:
        await callback_query.edit_message_text('Could not find this book 🤷‍♂️')






