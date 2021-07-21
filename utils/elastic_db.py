from elasticsearch import AsyncElasticsearch
from utils.Scaper import *
from pyrogram.types import *
from os import environ
es = AsyncElasticsearch()


def mapper(query:Book):
    return     {
        "book_id": query.id,
        "title": query.Title,
        "subtitle": query.subtitle,
        "isbn": query.Isbn,
        "pages": query.Pages,
        "year": query.Year,
        "publisher": query.Publisher,
        "categories": query.Publisher
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
                    "title",
                    "title._20gram",
                    "title._2gram"
                ],
                "fuzzy_transpositions": "true"
                , "fuzziness": 1
            }
        }
    }
    resp = await es.search(
        index="documents",
        body=body,
        size=10,
    )
    print(resp)
