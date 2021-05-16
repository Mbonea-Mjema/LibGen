import os
books_api_image = "http://books.google.com/books/content?id={}&printsec=frontcover&img=1&zoom=1&source=gbs_api"
books_api_call = "https://www.googleapis.com/books/v1/volumes?q={}&key="+os.environ["books_api"]
channel_message_link = "https://t.me/"+os.environ["telegram channel"]+"/{}"
