import os
books_api=os.env['books_api']
channel_name = os.env['channel_name'].replace()
books_api_image = "http://books.google.com/books/content?id={}&printsec=frontcover&img=1&zoom=1&source=gbs_api"
books_api_call = f"https://www.googleapis.com/books/v1/volumes?q={}&key={books_api}"
channel_message_link = f"https://t.me/{channel_name}/{}"



AIzaSyBbphNVAq9wGTsSMQAqRmmKxvTgjllrQNA