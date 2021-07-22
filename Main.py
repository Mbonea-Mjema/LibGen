from pyrogram import Client
import  os
from dotenv import load_dotenv
load_dotenv()
books_bot = Client(
    session_name='books_bot',
    bot_token=os.environ["BOT_TOKEN"],
    api_id=os.environ["API_ID"],
    api_hash=os.environ["API_HASH"],
    config_file="./Keys/config.ini"
)

if __name__ == "__main__":
    books_bot.run()
