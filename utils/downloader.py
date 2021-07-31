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


async  def api_query(query):
    query=urllib.parse.quote_plus(query)
    url = f"https://openlibrary.org/search.json?q={query}"
    async with ClientSession() as session:

        async with session.get(url) as response:
            data = await response.json()
        if data['docs'] != None:
            try:
                return data["docs"][0]["isbn"]
            except:
                return  None

