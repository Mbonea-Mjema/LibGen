import pprint

from elasticsearch import AsyncElasticsearch
from utils.DbModels import *
from pyrogram.types import *
from os import environ
es = AsyncElasticsearch( hosts=[environ['elastic_url']])


def mapper(query:Library):
    return     {
        "book_id": query.id,
        "title": query.Title,
        "subtitle": query.Subtitle,
        "isbn": query.Isbn,
        "pages": query.Pages,
        "year": query.Year,
        "publisher": query.Publisher,
        "categories": query.Categories
    }




async  def add_2index(query:Book,message:Message):
    body=mapper(query)
    resp = await  es.index(
    index=environ['elastic_index'],
    id = message.message_id,
    body = body
    )

    print(resp)

async  def book_lookup(query:Book):
    body ={
        "query": {
            "multi_match": {
                "query": query.Title,
                "type": "bool_prefix",
                "fields": [
                    'book_id'
                ],
            }
        }
    }
    print(query.id)
    body={
        "query": {
            "term": {
                "book_id": {
                    "value": query.id
                }
            }
        }
    }
    resp = await es.search(
        index=environ['elastic_index'],
        body=body,
        size=10,
    )
    pprint.pprint(resp)
    if resp['hits']['total']['value']> 0:
        return resp['hits']['hits'][0]
