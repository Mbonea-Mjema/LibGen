from pyrogram import Client

token = "1705162095:AAEnIkCdAwvI4WDqM9AthSgcOlW_fPc7yrA"
search_bot = Client("pdf", config_file="./Keys/config.ini", bot_token=token)

if __name__ == "__main__":
    search_bot.run()
