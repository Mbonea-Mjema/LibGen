from pyrogram import Client
import  os

books_bot = Client(
    bot_token=os.environ["BOT_TOKEN"],
    api_id=os.environ["API_ID"],
    api_hash=os.environ["API_HASH"],
    config_file="./Keys/config.ini"
)

if __name__ == "__main__":
    books_bot.run()
