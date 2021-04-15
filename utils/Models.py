from dataclasses import dataclass,asdict
from pyrogram.types import InputTextMessageContent,InlineQueryResultArticle
from uuid import uuid4
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)


@dataclass
class Book:
    id:str=None
    Title:str=None
    subtitle:str =None
    description:str=None
    Author:str =None
    Cover: str =None
    Year:str =None




class LibgenResult(Book):
    def __init__(self,result:dict):
        self.Title = result['Title']
        self.Author= result['Author']
        self.Language= result['Language']
        self.Year= result['Year']
        self.Size = result['Size']
        self.Type= result['Extension']
        self.Link= result['Mirror_1']


def message_gen(book:Book):
    book_dict=asdict(book)
    text =''
    for key,value in book_dict.items():
        if key=='Cover':
            text+=f'[Cover]({value})\n'
        elif key == 'Title':
            text += f'{key}:***{value}***' + '\n'
        else:
            if value!= None:
                if len(value)>20:
                    text += f'{key}:{value}'+'\n'
                else:
                    text += f'{key}:{value[:20]}...' + '\n'
    return text

class SearchResult:
    def __init__(self,book:Book):
        self.title = f'{book.Title}: {book.subtitle}'
        self.thumb = book.Cover
        self.description = book.description
        self.message_content = InputTextMessageContent(message_gen(book),disable_web_page_preview=False)
        self.article =InlineQueryResultArticle(id=uuid4(), title=book.Title, thumb_url=self.thumb, description=self.description,
                                 input_message_content=self.message_content)
