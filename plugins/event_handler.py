from pyrogram.types import *
from pyrogram import Client,emoji,filters

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)


@Client.on_message(filters=filters.command(['start'],prefixes='/'))
async def handle_start(message:Message):
    await message.reply_text("What's up")
    print('hello')
