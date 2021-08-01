from aiohttp import ClientSession
from bs4 import BeautifulSoup
import os,urllib

from uuid import uuid4


async def download_book(url, file_name, extension, id):
    cwd = os.getcwd()
    Download_dir = os.path.join(cwd, "Downloads")
    if not os.path.exists(Download_dir):
        os.mkdir(Download_dir)
    file_path = f"{Download_dir}/{id}.{extension}"
    print(file_path)
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        link = soup.find("h2").a["href"]
        async with session.get(link) as response:
            with open(file_path, "wb") as fd:
                async for data in response.content.iter_chunked(1024):
                    fd.write(data)

    return file_path


async  def api_query(title,author):
    title=urllib.parse.quote_plus(title)
    author=urllib.parse.quote_plus(author)
    url = f"https://openlibrary.org/search.json?title={title}&author={author}"
    async with ClientSession() as session:

        async with session.get(url) as response:
            data = await response.json()
        if data['docs'] != None:
            try:
                isbns =[]

                for book in data["docs"][:3]:
                    try:
                        print(book['title'],book['isbn'])
                    except:
                        continue
                    if book['isbn']:
                        isbns.extend(book['isbn'][:3])
                return isbns
            except:
                return  None

