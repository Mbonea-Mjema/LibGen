from pyrogram.types import *
from pyrogram import Client, emoji, filters
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger(__name__)

default_keyboard =InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Search For a book",
                   
                )
            ]
        ]
    )



@Client.on_message(filters.command(["start"], prefixes="/"))
async def handle_start(_, message: Message):
    await message.reply_text("I got books yo!", reply_markup=default_keyboard)
