import json
from pathlib import Path
from typing import List


from pydantic import BaseModel
from pybackpack.datastores import RedisDataStore

books_json_file = Path(__file__).parent / "test_datastores_books.json"


class ChildModel(BaseModel):
    name: str
    age: int


class ParentModel(BaseModel):
    name: str
    age: int
    children: List[ChildModel]

    class Config:
        schema_extra = {"persist_schema": "parent"}


def test_redis_ping():
    redis = RedisDataStore()
    assert redis.ping() is True


def test_redis_simple_get_set():
    redis = RedisDataStore()

    redis.set_str("key1", "value1")
    assert redis.get_str("key1") == "value1"

    redis.delete("key1")
    assert redis.get_str("key1") is None


def test_keys():
    root_prefix = "test"
    delimiter = ":"
    redis = RedisDataStore(root_prefix=root_prefix, prefix_delimiter=delimiter)

    redis.set_str("key1", "value1")
    redis.set_str("key2", "value1")
    keys = redis.keys("key*")
    assert len(keys) == 2

    redis.delete("key2")
    redis.delete("key1")

    # Test with root prefix
    redis = RedisDataStore(root_prefix=root_prefix, prefix_delimiter=delimiter)
    redis.set_str("key1", "value1")
    keys = redis.keys("key*")
    assert len(keys) == 1
    assert keys[0].decode("utf-8") == f"{root_prefix}{delimiter}key1"
    redis.delete("key1")

    # Test wihtout root prefix (default)
    redis = RedisDataStore(root_prefix=None, prefix_delimiter=delimiter)
    redis.set_str("key1", "value1")
    keys = redis.keys("key*")
    assert keys[0].decode("utf-8") == "key1"
    redis.delete("key1")

    # Test wiht empty root prefix
    redis = RedisDataStore(root_prefix="", prefix_delimiter=delimiter)
    redis.set_str("key1", "value1")
    keys = redis.keys("key*")
    assert keys[0].decode("utf-8") == ":key1"
    redis.delete("key1")

    # Test json keys
    redis = RedisDataStore(root_prefix=root_prefix, prefix_delimiter=delimiter)
    redis.set_json("key1", {"name": "value1"})
    keys = redis.keys("*")
    assert len(keys) == 1
    assert keys[0].decode("utf-8") == f"{root_prefix}{delimiter}key1"
    redis.delete("key1")

    # Test pydantic keys
    redis = RedisDataStore(root_prefix=root_prefix, prefix_delimiter=delimiter)
    redis.set_pydantic("key1", ParentModel(name="value1", age=10, children=[]))
    keys = redis.keys("*")
    assert len(keys) == 1
    persist_schema = ParentModel.Config.schema_extra["persist_schema"]
    assert (
        keys[0].decode("utf-8")
        == f"{root_prefix}{delimiter}{persist_schema}{delimiter}key1"
    )
    redis.delete_pydantic("key1", ParentModel)

    # Test pydantic keys without root prefix
    redis = RedisDataStore(root_prefix=None, prefix_delimiter=delimiter)
    redis.set_pydantic("key1", ParentModel(name="value1", age=10, children=[]))
    redis.set_pydantic("key2", ParentModel(name="value2", age=20, children=[]))
    keys = redis.keys("*key*")
    assert len(keys) == 2
    persist_schema = ParentModel.Config.schema_extra["persist_schema"]
    assert keys[0].decode("utf-8") == f"{persist_schema}{delimiter}key2"

    # Clean up
    for key in redis.keys("*key*"):
        redis.delete(key)


def test_redis_json():
    redis = RedisDataStore()

    parent = {
        "name": "parent",
        "age": 50,
        "children": [
            {"name": "child1", "age": 10},
            {"name": "child2", "age": 20},
        ],
    }

    # Set and get the parent
    redis.set_json("p1", parent)
    name = redis.get_json("p1", "$.name")
    assert name == "parent"

    # Update the name of the first child
    redis.set_json("p1", "child1-updated", "$.children[0].name")
    name = redis.get_json("p1", "$.children[0].name")
    assert name == "child1-updated"

    # Update the whole object of the first child
    new_child = {"name": "child1-updated2", "age": 11}
    redis.set_json("p1", new_child, "$.children[0]")
    loaded_child = redis.get_json("p1", "$.children[0]")
    assert loaded_child["name"] == "child1-updated2"

    # Delete the first child
    redis.delete_json("p1", "$.children[0]")
    loaded_parent = redis.get_json("p1")
    assert len(loaded_parent["children"]) == 1

    # Delete the parent
    redis.delete("p1")
    assert redis.get_json("p1") is None


def test_redis_from_pydantic_dict():
    redis = RedisDataStore()

    parent = ParentModel(
        name="parent",
        age=50,
        children=[
            ChildModel(name="child1", age=10),
            ChildModel(name="child2", age=20),
        ],
    )

    # Set the parent and childrens
    redis.set_json("p1", parent.model_dump())
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.name == "parent"
    assert len(loaded_parent.children) == 2
    assert loaded_parent.children[0].name == "child1"

    # Update the name of the first child
    redis.set_json("p1", "child1-updated", "$.children[0].name")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated"

    # Update the name using the object of the first child
    loaded_parent.children[0].name = "child1-updated-again"
    redis.set_json(
        "p1", loaded_parent.children[0].model_dump(), "$.children[0]"
    )
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated-again"

    # Update the whole object of the first child
    redis.set_json(
        "p1", {"name": "child1-updated", "age": 11}, "$.children[0]"
    )
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated"
    assert loaded_parent.children[0].age == 11

    # Update the whole object of the first child using the object
    updated_child = ChildModel(name="child1-updated2", age=12)
    redis.set_json("p1", updated_child.model_dump(), "$.children[0]")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated2"

    # Update the first child and add the third child.
    loaded_parent.children[0] = ChildModel(name="child1-updated3", age=13)
    loaded_parent.children.append(ChildModel(name="child3", age=30))
    redis.set_json("p1", loaded_parent.model_dump(), "$")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated3"
    assert loaded_parent.children[2].name == "child3"

    # Get the second child only
    loaded_child = ChildModel(**redis.get_json("p1", "$.children[1]"))
    assert loaded_child.name == "child2"
    assert loaded_child.age == 20

    # Remove the first child
    redis.delete_json("p1", "$.children[0]")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert len(loaded_parent.children) == 2

    # delete the parent
    redis.delete("p1")
    assert redis.get_json("p1") is None


def test_redis_pydantic():
    redis = RedisDataStore()

    parent = ParentModel(
        name="parent",
        age=50,
        children=[
            ChildModel(name="child1", age=10),
            ChildModel(name="child2", age=20),
        ],
    )

    # Set and get the parent
    redis.set_pydantic("p1", parent)
    loaded_parent = redis.get_pydantic("p1", ParentModel)
    assert loaded_parent.name == "parent"
    assert len(loaded_parent.children) == 2

    # Update the name of the first child
    parent.children[0].name = "child1-updated"
    redis.set_pydantic("p1", parent)
    loaded_parent = redis.get_pydantic("p1", ParentModel)
    assert loaded_parent.children[0].name == "child1-updated"

    redis.delete_pydantic("p1", ParentModel)
    assert redis.get_pydantic("p1", ParentModel) is None


def test_redis_create_index():
    root_prefix = "test"
    redis = RedisDataStore(root_prefix=root_prefix)

    schema = [
        {"field": "$.name", "type": "text", "alias": "name"},
        {"field": "$.age", "type": "number", "alias": "age"},
    ]

    index_name = "parents"
    # Get index info
    index_info = redis.get_index_info(index_name)
    if index_info:
        assert index_info["index_name"] == "test:idx:parents"
        print(index_info["index_definition"])
        # Drop the index
        redis.delete_index(index_name)

    # Create the index
    redis.create_index_on_json(
        index_name=index_name,
        key_prefixes_to_index=["parents"],
        schema=schema,
    )
    index_info = redis.get_index_info(index_name)
    assert (
        index_info["index_definition"][3][0].decode("utf-8")
    ) == "test:parents:"
    assert redis.get_index_info(index_name) is not None

    # Delete the index
    redis.delete_index(index_name)
    assert redis.get_index_info(index_name) is None


def test_redis_search_on_json():
    # Load books fromt the test json file
    with open(books_json_file, "r", encoding="utf-8") as file:
        books = json.load(file)

    redis = RedisDataStore()

    # Remove all the books in redis
    for key in redis.keys("book*"):
        redis.delete(key)

    # Set the books in redis
    for book in books:
        redis.set_json(f"book:{book['id']}", book)

    index_name = "books"

    # Delet the index if already exists
    if redis.get_index_info(index_name):
        redis.delete_index(index_name)

    # Create index
    schema = [
        {"field": "$.title", "type": "text", "alias": "title"},
        {"field": "$.year", "type": "number", "alias": "year"},
        {"field": "$.description", "type": "text", "alias": "description"},
        {"field": "$.topics", "type": "tag", "alias": "topics"},
        {
            "field": "$.authors[*].first_name",
            "type": "text",
            "alias": "author_first_name",
        },
        {
            "field": "$.authors[*].last_name",
            "type": "text",
            "alias": "author_last_name",
        },
        {
            "field": "$.authors[*].born",
            "type": "number",
            "alias": "author_born",
        },
    ]

    redis.create_index_on_json(
        index_name=index_name, schema=schema, key_prefixes_to_index=["book"]
    )

    # Check if index is created and get the index info
    index_info = redis.get_index_info(index_name)
    assert index_info["index_name"] == "idx:books"

    # Search for an unknown title
    result = redis.search_on_json(index_name=index_name, query="unknown")
    assert len(result) == 0

    # Search for a known title
    result = redis.search_on_json(index_name=index_name, query="Deep Learning")
    assert len(result) == 1

    # Search for a partial name
    result = redis.search_on_json(index_name=index_name, query="Deep")
    assert len(result) == 1

    # Search for all books between 2015 and 2024
    result = redis.search_on_json(
        index_name=index_name, query="@year:[2015 2024]"
    )
    assert len(result) == 3
    assert {
        "Deep Learning",
        "Introduction to Linear Algebra 5th Edition",
        "Introduction to Algorithms 4th Edition",
    } <= {r["title"] for r in result}

    # Find all books which at least one of their authors born betwen a range
    result = redis.search_on_json(
        index_name=index_name, query="@author_born:[1980 1990]"
    )
    assert len(result) == 1
    assert result[0]["title"] == "Deep Learning"

    # Find all books which at least related to one of the topics
    result = redis.search_on_json(
        index_name=index_name, query="@topics:{physics}"
    )
    assert len(result) == 2

    # Find all books which are related to multiple topics AND togther.
    result = redis.search_on_json(
        index_name=index_name, query="@topics:{linear algebra} @topics:{math}"
    )
    assert len(result) == 1
    assert {
        "Introduction to Linear Algebra 5th Edition",
    } <= {r["title"] for r in result}

    # Find all books which are related to either of topics, OR together.
    result = redis.search_on_json(
        index_name=index_name, query="@topics:{linear algebra|physics}"
    )
    assert len(result) == 3
    assert {
        "A Brief History of Time",
        "Introduction to Linear Algebra 5th Edition",
    } <= {r["title"] for r in result}

    # Find all books which their description contains "comprehensive" and the \
    # title doesn't contain "Deep"
    result = redis.search_on_json(
        index_name=index_name,
        query="@description:comprehensive -@title:Deep",
    )
    assert len(result) == 1
    assert result[0]["title"] == "Introduction to Linear Algebra 5th Edition"

    # Clean up
    redis.delete_index(index_name)
    for key in redis.keys("book*"):
        redis.delete(key)
