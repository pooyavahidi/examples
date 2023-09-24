import json
from pathlib import Path
from typing import List, Optional
import pytest
from pydantic import BaseModel
from pybackpack.datastores.mongo import MongoDataStore


class Author(BaseModel):
    first_name: str
    last_name: str
    born: int


class Book(BaseModel):
    id: int
    title: str
    year: int
    authors: List[Author]
    topics: List[str]
    description: Optional[str] = None

    class Config:
        schema_extra = {"persist_schema": "book"}


@pytest.fixture
def books_dict():
    books_json_file = Path(__file__).parent / "books.json"
    with open(books_json_file, "r", encoding="utf-8") as file:
        books = json.load(file)
    return books


@pytest.fixture
def mongo():
    # Set Up
    mongo_ds = MongoDataStore("pybackpack")

    # Clean up the database before the test
    # drop all the collections
    for collection_name in mongo_ds.db.list_collection_names():
        mongo_ds.db.drop_collection(collection_name)

    yield mongo_ds


@pytest.fixture
def books_col(mongo, books_dict):
    col = mongo.collection("books")
    col.insert_many(books_dict)

    yield col

    col.drop()


def test_mongo_crud(mongo, books_dict):
    db = mongo.db

    collection_name = "books"
    col = mongo.collection(collection_name)

    # Insert documents
    for book in books_dict:
        res = col.insert_one(book)
        assert res.acknowledged
        assert res.inserted_id

    # Delete one document by
    res = col.delete_many({"id": 1})
    assert res.acknowledged
    assert res.deleted_count == 1

    # Count all the documents in the collection
    res = col.count_documents({})
    assert res == len(books_dict) - 1

    # Count of the documents in the collection with a query
    res = col.count_documents({"title": "A Brief History of Time"})
    assert res == 1

    # Get the documents in the collection
    res = col.find({"title": "A Brief History of Time"})
    assert res[0]["id"] == 4
    assert res[0]["year"] == 1988
    assert res[0]["title"] == "A Brief History of Time"
    assert res[0]["authors"][0]["last_name"] == "Hawking"
    assert len(list(res)) == 1

    # Update a document partially
    res = col.update_many({"id": 4}, {"$set": {"title": "ABHOT"}})
    assert res.acknowledged
    assert res.matched_count == 1
    assert res.modified_count == 1

    # Read the updated document
    res = col.find({"id": 4})
    assert res[0]["title"] == "ABHOT"
    assert res[0]["authors"][0]["first_name"] == "Stephen"

    # Replace a document completely
    # Note: the the schema is changed here.
    new_book = {
        "title": "ABHOT",
        "id": 4,
        "authors": [{"name": "Stephen Hawking"}],
    }
    res = col.replace_one({"id": 4}, new_book)
    assert res.acknowledged
    assert res.matched_count == 1
    assert res.modified_count == 1

    # Get the updated document
    res = col.find({"id": 4})
    assert res[0]["id"] == 4
    assert res[0]["title"] == "ABHOT"
    assert res[0]["authors"][0]["name"] == "Stephen Hawking"
    assert res[0].get("description") is None
    assert len(list(res)) == 1

    # delete all using delete_many
    res = col.delete_many({})
    assert res.acknowledged
    assert res.deleted_count == len(books_dict) - 1

    # delete the collection altogether
    col.drop()
    res = db.list_collection_names()
    assert collection_name not in res


def test_pydantic_crud(mongo, books_dict):
    # Create pydantic models for books using books_dict
    books = [Book(**book) for book in books_dict]
    assert len(books) == len(books_dict)
    assert books[0].title == "Deep Learning"
    assert len(books[0].authors) == 3

    # Create a new collection
    col = mongo.collection_for_pydantic(Book)

    # Insert documents
    res = col.insert_many([b.model_dump() for b in books])
    assert res.acknowledged
    assert len(res.inserted_ids) == len(books)

    # Get one book by query
    res = col.find({"id": 1})
    book = Book(**res[0])
    assert book.title == "Deep Learning"

    # Get all books
    res = col.find({})
    assert len(list(res)) == len(books)

    # Update a book using pymongo collection directly.
    res = col.update_many(
        {"id": 1}, {"$set": {"title": "Deep Learning 2nd Ed."}}
    )
    assert res.acknowledged
    assert res.matched_count == 1
    assert res.modified_count == 1

    # Get the updated book
    res = col.find({"id": 1})
    book = Book(**res[0])
    assert book.title == "Deep Learning 2nd Ed."

    # Delete an author from book 1
    res = col.update_many({"id": 1}, {"$pop": {"authors": 1}})
    assert res.modified_count == 1

    # Get the updated book
    res = col.find({"id": 1})
    book = Book(**res[0])
    assert len(book.authors) == 2

    # Count all books which have author born between 1980 and 1990
    res = col.count_documents({"authors.born": {"$gte": 1960, "$lte": 1990}})
    assert res == 2

    # Remove all the authors where born is between 1960 and 1990
    # The filter instead of {} could be set like this:
    # {"authors.born": {"$gte": 1960, "$lte": 1990}},
    res = col.update_many(
        {},
        {"$pull": {"authors": {"born": {"$gte": 1960, "$lte": 1990}}}},
    )


def test_mongo_query(books_col):
    # Get an unknown title
    res = books_col.find({"title": "Unknown"})
    res = list(res)
    assert len(res) == 0

    # Get a known title
    res = books_col.find({"title": "A Brief History of Time"})
    res = list(res)
    assert len(res) == 1

    # Get a known title with a query, using "i" option for case-insensitive
    res = books_col.find({"title": {"$regex": "deep", "$options": "i"}})
    assert res[0]["title"] == "Deep Learning"

    # Search for all books between 2015 and 2024
    res = books_col.find({"year": {"$gte": 2015, "$lte": 2024}})
    assert {
        "Deep Learning",
        "Introduction to Linear Algebra 5th Edition",
        "Introduction to Algorithms 4th Edition",
    } <= {r["title"] for r in res}

    # Find all books which at least one of their authors born between a range
    res = books_col.find({"authors.born": {"$gte": 1980, "$lte": 1990}})
    assert res[0]["title"] == "Deep Learning"
    assert len(list(res)) == 1

    # Find all books which at least related to one of the topics
    res = books_col.find({"topics": {"$in": ["physics"]}})
    res = list(res)
    assert len(res) == 2

    # Find all the books which the first name of the first author is Stephen
    res = books_col.find({"authors.first_name": "Stephen"})
    assert res[0]["title"] == "A Brief History of Time"
    assert len(list(res)) == 2

    # Final all the books which the last name of their authors starts with C
    res = books_col.find({"authors.last_name": {"$regex": "^C"}})
    res = list(res)
    assert len(res) == 2
    assert {"Introduction to Algorithms 4th Edition", "Deep Learning"} == {
        r["title"] for r in res
    }
    assert len(res[0]["authors"]) == 3

    # Use paging and sorting to get the first book sorted by year descending
    res = books_col.find(
        {"topics": {"$in": ["physics"]}},
        limit=1,
        sort=[("year", -1)],
    )
    assert res[0]["title"] == "The Nature of Space and Time"

    # Find books using multiple ids
    res = books_col.find({"id": {"$in": [1, 2, 3]}})
    assert len(list(res)) == 3


def test_mongo_query_projection(books_col):
    # Get all the books with only title and year
    res = books_col.find({}, {"title": 1, "year": 1})
    res = list(res)
    assert res[0]["title"] == "Deep Learning"
    assert res[0]["year"] == 2016
    assert res[0].get("authors") is None
    assert len(res) == 5

    # Get only the first_name of the authors for the books which has 1 author
    res = books_col.find({"authors": {"$size": 1}}, {"authors.first_name": 1})
    res = list(res)
    assert len(res) == 2

    # Get list of institutions for authors which born before 1960 and their
    # books is published in 2022
    res = books_col.find(
        {"authors.born": {"$lt": 1960}, "year": 2022},
        {"authors.institutions": 1},
    )
    res = list(res)
    assert len(res) == 1
    # Note that regardless of the filter to get only authors born before 1960,
    # MongoDB returns all the authors for this book because MongoDB doesn't
    # inherently filter the inner array elements based on the conditions
    # provided. Instead, it uses those conditions to decide whether the entire
    # `document`` (including all sub-documents in the documents field) should
    # be returned. Hence the number of authors is 4.
    assert len(res[0]["authors"]) == 4

    # Use $filter operator and aggregation pipeline
    pipeline = [
        {"$match": {"year": 2022}},
        {
            "$project": {
                "authors": {
                    "$filter": {
                        "input": "$authors",
                        "as": "author",
                        "cond": {"$lt": ["$$author.born", 1960]},
                    }
                }
            }
        },
    ]

    res = books_col.aggregate(pipeline)
    res = list(res)
    assert len(res) == 1
    # Now, only the authors born before 1960 should be in the result.
    assert len(res[0]["authors"]) == 3
